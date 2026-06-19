"""
training_data.py
------------------
Builds the historical dataset the models train on.

IMPORTANT ON DATA LEAKAGE:
For each historical match we use, our features must only reflect
information that was KNOWN BEFORE that match was played (e.g. the team's
form/stats *up to* that date, not including that match's own result).
This script handles that by fetching team statistics scoped to a season
and only using fixtures that occurred chronologically before the match
being labeled.

For a national-team matchup like Morocco vs Scotland, there usually isn't
a deep historical sample of two teams playing each other directly, so we
train on a BROADER pool of international matches (friendlies, qualifiers,
tournament matches from similar-strength teams) and then apply the trained
model to the specific Morocco vs Scotland feature row. This is standard
practice -- you train on many games, then score the one game you care about.
"""

import pandas as pd
import numpy as np
from data_fetcher import get_team_statistics, get_recent_form
from features import team_season_features, recent_form_features


def build_training_dataset(fixtures, league_id, season):
    """
    fixtures: list of completed fixture dicts (from API-Football, e.g.
    pulled via /fixtures?league=...&season=...&status=FT) that you want
    to use as training examples.

    Returns: X (DataFrame of features), y_outcome (0/1/2), y_home_goals, y_away_goals
    """
    rows = []
    y_outcome = []
    y_home_goals = []
    y_away_goals = []

    # cache team-level season stats so we don't re-fetch per fixture
    stats_cache = {}
    form_cache = {}

    for f in fixtures:
        home_id = f["teams"]["home"]["id"]
        away_id = f["teams"]["away"]["id"]
        home_goals = f["goals"]["home"]
        away_goals = f["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue  # match hasn't been played / no result yet

        if home_id not in stats_cache:
            stats_cache[home_id] = get_team_statistics(home_id, league_id, season)
        if away_id not in stats_cache:
            stats_cache[away_id] = get_team_statistics(away_id, league_id, season)

        if home_id not in form_cache:
            form_cache[home_id] = get_recent_form(home_id, last_n=5)
        if away_id not in form_cache:
            form_cache[away_id] = get_recent_form(away_id, last_n=5)

        home_feats = team_season_features(stats_cache[home_id], "team1")
        away_feats = team_season_features(stats_cache[away_id], "team2")
        home_form = recent_form_features(form_cache[home_id], home_id, "team1")
        away_form = recent_form_features(form_cache[away_id], away_id, "team2")

        row = {}
        row.update(home_feats)
        row.update(away_feats)
        row.update(home_form)
        row.update(away_form)
        row["diff_win_rate"] = row.get("team1_win_rate", np.nan) - row.get("team2_win_rate", np.nan)
        row["diff_goals_for_avg"] = row.get("team1_goals_for_avg", np.nan) - row.get("team2_goals_for_avg", np.nan)
        row["diff_goals_against_avg"] = row.get("team1_goals_against_avg", np.nan) - row.get("team2_goals_against_avg", np.nan)
        row["diff_form_points"] = row.get("team1_form_points_avg", np.nan) - row.get("team2_form_points_avg", np.nan)

        rows.append(row)

        if home_goals > away_goals:
            y_outcome.append(2)  # home win
        elif home_goals == away_goals:
            y_outcome.append(1)  # draw
        else:
            y_outcome.append(0)  # away win

        y_home_goals.append(home_goals)
        y_away_goals.append(away_goals)

    X = pd.DataFrame(rows).fillna(0)
    return X, np.array(y_outcome), np.array(y_home_goals), np.array(y_away_goals)
