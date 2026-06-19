"""
features.py
------------
Turns raw API responses into a single feature row per match,
combining team-level, player-level, and venue-level signals.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# TEAM-LEVEL FEATURES
# ---------------------------------------------------------------------------

def team_season_features(stats_json, prefix):
    """
    Extract win rate, goals scored/conceded averages, clean sheet rate
    from API-Football's teams/statistics response.
    """
    if not stats_json:
        return {
            f"{prefix}_win_rate": np.nan,
            f"{prefix}_goals_for_avg": np.nan,
            f"{prefix}_goals_against_avg": np.nan,
            f"{prefix}_clean_sheet_rate": np.nan,
        }

    fixtures = stats_json.get("fixtures", {})
    played = fixtures.get("played", {}).get("total", 0) or 1  # avoid div/0
    wins = fixtures.get("wins", {}).get("total", 0)

    goals = stats_json.get("goals", {})
    goals_for_avg = float(goals.get("for", {}).get("average", {}).get("total", 0) or 0)
    goals_against_avg = float(goals.get("against", {}).get("average", {}).get("total", 0) or 0)

    clean_sheets = stats_json.get("clean_sheet", {}).get("total", 0)

    return {
        f"{prefix}_win_rate": wins / played,
        f"{prefix}_goals_for_avg": goals_for_avg,
        f"{prefix}_goals_against_avg": goals_against_avg,
        f"{prefix}_clean_sheet_rate": clean_sheets / played,
    }


def recent_form_features(fixtures_list, team_id, prefix, last_n=5):
    """
    Weight recent matches (last 5) more heavily than season-long stats.
    Returns form points (3=win,1=draw,0=loss) averaged, and recent goal diff.
    """
    fixtures_list = fixtures_list[-last_n:] if fixtures_list else []
    if not fixtures_list:
        return {f"{prefix}_form_points_avg": np.nan, f"{prefix}_form_goal_diff_avg": np.nan}

    points = []
    goal_diffs = []
    for f in fixtures_list:
        home_id = f["teams"]["home"]["id"]
        away_id = f["teams"]["away"]["id"]
        home_goals = f["goals"]["home"] or 0
        away_goals = f["goals"]["away"] or 0

        is_home = (home_id == team_id)
        team_goals = home_goals if is_home else away_goals
        opp_goals = away_goals if is_home else home_goals

        if team_goals > opp_goals:
            points.append(3)
        elif team_goals == opp_goals:
            points.append(1)
        else:
            points.append(0)
        goal_diffs.append(team_goals - opp_goals)

    return {
        f"{prefix}_form_points_avg": np.mean(points),
        f"{prefix}_form_goal_diff_avg": np.mean(goal_diffs),
    }


def head_to_head_features(h2h_fixtures, team1_id, prefix="h2h"):
    """
    Historical head-to-head record from team1's perspective.
    """
    if not h2h_fixtures:
        return {f"{prefix}_team1_win_rate": np.nan, f"{prefix}_avg_goal_diff": np.nan}

    wins = 0
    goal_diffs = []
    for f in h2h_fixtures:
        home_id = f["teams"]["home"]["id"]
        home_goals = f["goals"]["home"] or 0
        away_goals = f["goals"]["away"] or 0

        team1_is_home = (home_id == team1_id)
        team1_goals = home_goals if team1_is_home else away_goals
        opp_goals = away_goals if team1_is_home else home_goals

        if team1_goals > opp_goals:
            wins += 1
        goal_diffs.append(team1_goals - opp_goals)

    return {
        f"{prefix}_team1_win_rate": wins / len(h2h_fixtures),
        f"{prefix}_avg_goal_diff": np.mean(goal_diffs),
    }


# ---------------------------------------------------------------------------
# PLAYER-LEVEL FEATURES  (the "who's actually likely to play" upgrade)
# ---------------------------------------------------------------------------

def player_weighted_strength(squad, player_stats_lookup, start_prob_lookup, prefix):
    """
    squad: list of player dicts from get_squad()
    player_stats_lookup: dict {player_id: avg_rating}
    start_prob_lookup: dict {player_id: probability_of_starting} (0-1)

    This is the core upgrade over the original reel's model:
    instead of one flat team-average rating, each player's individual
    rating is WEIGHTED by how likely they are to actually start.
    A star player who's injured/suspended contributes much less;
    a confirmed starter in great form contributes a lot.
    """
    weighted_ratings = []
    total_weight = 0

    for p in squad:
        pid = p["id"]
        rating = player_stats_lookup.get(pid, 6.5)       # default "average" rating
        start_prob = start_prob_lookup.get(pid, 0.0)      # default: not starting

        weighted_ratings.append(rating * start_prob)
        total_weight += start_prob

    if total_weight == 0:
        squad_strength = np.mean(list(player_stats_lookup.values())) if player_stats_lookup else 6.5
    else:
        squad_strength = sum(weighted_ratings) / total_weight

    return {f"{prefix}_squad_strength": squad_strength}


def estimate_start_probability(player_minutes_last5, max_possible_minutes=450):
    """
    Simple heuristic: probability of starting next match
    based on how many minutes they've played in the last 5 games.
    (You can swap this for actual confirmed-lineup data once it's announced,
    usually ~1 hour before kickoff.)
    """
    return min(player_minutes_last5 / max_possible_minutes, 1.0)


# ---------------------------------------------------------------------------
# VENUE / PITCH FEATURES
# ---------------------------------------------------------------------------

def venue_features(venue_history_df, team_id, prefix):
    """
    venue_history_df: DataFrame of past matches played at this specific venue,
    columns: ['team_id','goals_for','goals_against','result']

    Captures things like: "this pitch tends to produce low-scoring games"
    or "Team X has a strong record at this specific venue".
    """
    if venue_history_df is None or venue_history_df.empty:
        return {
            f"{prefix}_venue_win_rate": np.nan,
            f"{prefix}_venue_avg_goals_for": np.nan,
            f"venue_avg_total_goals": np.nan,
        }

    team_rows = venue_history_df[venue_history_df["team_id"] == team_id]
    win_rate = (team_rows["result"] == "W").mean() if not team_rows.empty else np.nan
    avg_gf = team_rows["goals_for"].mean() if not team_rows.empty else np.nan
    avg_total_goals = (venue_history_df["goals_for"] + venue_history_df["goals_against"]).mean()

    return {
        f"{prefix}_venue_win_rate": win_rate,
        f"{prefix}_venue_avg_goals_for": avg_gf,
        "venue_avg_total_goals": avg_total_goals,
    }


# ---------------------------------------------------------------------------
# COMBINE EVERYTHING INTO ONE FEATURE ROW
# ---------------------------------------------------------------------------

def build_match_feature_row(team1_features, team2_features, h2h_feats, venue_feats):
    """
    Merge all feature dicts into a single-row DataFrame ready for the model.
    Also computes head-to-head DIFFERENTIAL features, which tend to be more
    predictive than raw stats (e.g. win_rate_diff instead of two separate win rates).
    """
    row = {}
    row.update(team1_features)
    row.update(team2_features)
    row.update(h2h_feats)
    row.update(venue_feats)

    # Differential features (team1 minus team2) — usually the most predictive
    row["diff_win_rate"] = team1_features.get("team1_win_rate", np.nan) - team2_features.get("team2_win_rate", np.nan)
    row["diff_goals_for_avg"] = team1_features.get("team1_goals_for_avg", np.nan) - team2_features.get("team2_goals_for_avg", np.nan)
    row["diff_goals_against_avg"] = team1_features.get("team1_goals_against_avg", np.nan) - team2_features.get("team2_goals_against_avg", np.nan)
    row["diff_form_points"] = team1_features.get("team1_form_points_avg", np.nan) - team2_features.get("team2_form_points_avg", np.nan)
    row["diff_squad_strength"] = team1_features.get("team1_squad_strength", np.nan) - team2_features.get("team2_squad_strength", np.nan)

    return pd.DataFrame([row])
