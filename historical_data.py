"""
historical_data.py
--------------------
Loads REAL international football results (1872-2024, ~49,000 matches) from
a free, public GitHub CSV -- no API key, no signup, no rate limits, no
Kaggle account needed:

    https://raw.githubusercontent.com/martj42/international_results/master/results.csv

This replaces demo_data.py's fake/synthetic training data with actual match
history, which is what was capping our accuracy near random-guessing before.

IMPORTANT ON DATA LEAKAGE:
For every match used as a training example, each team's features (win rate,
goals avg, form) are computed using ONLY matches that happened BEFORE that
match's date. This is done via pandas groupby + shift, so the model never
"cheats" by seeing the future.
"""

import pandas as pd
import numpy as np

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"


def load_results(path_or_url=RESULTS_URL, min_year=2000):
    """
    Loads results.csv. Defaults to fetching the live GitHub copy.
    min_year filters out very old matches -- football has changed a lot
    since 1872, so training only on roughly-modern-era matches (2000+)
    keeps the patterns more relevant to today's game. Tune as you like;
    more data = more signal but also more "old game" noise.
    """
    df = pd.read_csv(path_or_url, parse_dates=["date"])
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")
    df = df.dropna(subset=["home_score", "away_score"]).copy()
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)
    df = df[df["date"].dt.year >= min_year].reset_index(drop=True)
    df["match_id"] = df.index
    return df


def _build_long_format(df):
    """
    Reshapes each match into two rows (one per team's perspective), so we
    can compute each team's rolling stats with simple groupby operations.
    """
    home = df[["match_id", "date", "home_team", "away_team", "home_score", "away_score"]].copy()
    home.columns = ["match_id", "date", "team", "opponent", "goals_for", "goals_against"]
    home["is_home"] = True

    away = df[["match_id", "date", "away_team", "home_team", "away_score", "home_score"]].copy()
    away.columns = ["match_id", "date", "team", "opponent", "goals_for", "goals_against"]
    away["is_home"] = False

    long_df = pd.concat([home, away], ignore_index=True)
    long_df = long_df.sort_values(["team", "date"]).reset_index(drop=True)

    long_df["points"] = np.where(
        long_df["goals_for"] > long_df["goals_against"], 3,
        np.where(long_df["goals_for"] == long_df["goals_against"], 1, 0)
    )
    return long_df


def _add_prior_features(long_df, form_window=5, avg_window=15):
    """
    For each team, computes win_rate/goals avgs (over last `avg_window`
    matches) and form_points_avg (over last `form_window` matches), using
    only PRIOR matches (shifted by 1) to avoid leakage.
    """
    g = long_df.groupby("team", group_keys=False)

    long_df["win"] = (long_df["goals_for"] > long_df["goals_against"]).astype(int)

    # shift(1) first so the current match's own result never leaks into its own features
    long_df["prior_win_rate"] = g["win"].apply(lambda s: s.shift(1).rolling(avg_window, min_periods=3).mean())
    long_df["prior_goals_for_avg"] = g["goals_for"].apply(lambda s: s.shift(1).rolling(avg_window, min_periods=3).mean())
    long_df["prior_goals_against_avg"] = g["goals_against"].apply(lambda s: s.shift(1).rolling(avg_window, min_periods=3).mean())
    long_df["prior_form_points_avg"] = g["points"].apply(lambda s: s.shift(1).rolling(form_window, min_periods=2).mean())

    return long_df


def build_training_dataset(df, form_window=5, avg_window=15):
    """
    Returns X (features), y_outcome (0=away win,1=draw,2=home win),
    y_home_goals, y_away_goals -- built entirely from real match history.
    """
    long_df = _build_long_format(df)
    long_df = _add_prior_features(long_df, form_window, avg_window)

    home_feats = long_df[long_df["is_home"]].set_index("match_id")[
        ["prior_win_rate", "prior_goals_for_avg", "prior_goals_against_avg", "prior_form_points_avg"]
    ].rename(columns=lambda c: "team1_" + c.replace("prior_", ""))

    away_feats = long_df[~long_df["is_home"]].set_index("match_id")[
        ["prior_win_rate", "prior_goals_for_avg", "prior_goals_against_avg", "prior_form_points_avg"]
    ].rename(columns=lambda c: "team2_" + c.replace("prior_", ""))

    merged = df.set_index("match_id").join(home_feats).join(away_feats)
    merged = merged.dropna(subset=[
        "team1_win_rate", "team2_win_rate", "team1_form_points_avg", "team2_form_points_avg"
    ])  # drop matches too early in a team's history to have prior stats

    merged["diff_win_rate"] = merged["team1_win_rate"] - merged["team2_win_rate"]
    merged["diff_goals_for_avg"] = merged["team1_goals_for_avg"] - merged["team2_goals_for_avg"]
    merged["diff_goals_against_avg"] = merged["team1_goals_against_avg"] - merged["team2_goals_against_avg"]
    merged["diff_form_points"] = merged["team1_form_points_avg"] - merged["team2_form_points_avg"]

    feature_cols = [
        "team1_win_rate", "team2_win_rate",
        "team1_goals_for_avg", "team2_goals_for_avg",
        "team1_goals_against_avg", "team2_goals_against_avg",
        "team1_form_points_avg", "team2_form_points_avg",
        "diff_win_rate", "diff_goals_for_avg", "diff_goals_against_avg", "diff_form_points",
    ]
    X = merged[feature_cols].reset_index(drop=True)

    y_outcome = np.where(merged["home_score"] > merged["away_score"], 2,
                  np.where(merged["home_score"] == merged["away_score"], 1, 0))
    y_home_goals = merged["home_score"].values
    y_away_goals = merged["away_score"].values

    return X, y_outcome, y_home_goals, y_away_goals


def get_current_team_stats(df, team_name, form_window=5, avg_window=15):
    """
    Real, up-to-date stats for a team based on their actual last N matches
    in the dataset -- used to build the live prediction's feature row.
    """
    long_df = _build_long_format(df)
    team_rows = long_df[long_df["team"] == team_name].sort_values("date")

    if team_rows.empty:
        raise ValueError(f"No matches found for team name '{team_name}' -- check exact spelling "
                          f"matches the dataset (e.g. 'United States' not 'USA').")

    recent = team_rows.tail(avg_window)
    form_recent = team_rows.tail(form_window)

    win_rate = (recent["goals_for"] > recent["goals_against"]).mean()
    goals_for_avg = recent["goals_for"].mean()
    goals_against_avg = recent["goals_against"].mean()
    form_points_avg = form_recent["points"].mean() if "points" in form_recent else np.where(
        form_recent["goals_for"] > form_recent["goals_against"], 3,
        np.where(form_recent["goals_for"] == form_recent["goals_against"], 1, 0)
    ).mean()

    return {
        "win_rate": win_rate,
        "goals_for_avg": goals_for_avg,
        "goals_against_avg": goals_against_avg,
        "form_points_avg": form_points_avg,
        "matches_used": len(recent),
        "last_match_date": team_rows["date"].max(),
    }


def get_head_to_head(df, team1, team2, last_n=10):
    """
    Real head-to-head record between two specific teams, computed directly
    from the dataset -- no manual guessing needed.
    """
    h2h = df[
        ((df["home_team"] == team1) & (df["away_team"] == team2)) |
        ((df["home_team"] == team2) & (df["away_team"] == team1))
    ].sort_values("date").tail(last_n)

    if h2h.empty:
        return {"team1_win_rate": np.nan, "avg_goal_diff": np.nan, "matches_found": 0}

    wins = 0
    goal_diffs = []
    for _, row in h2h.iterrows():
        if row["home_team"] == team1:
            t1_goals, t2_goals = row["home_score"], row["away_score"]
        else:
            t1_goals, t2_goals = row["away_score"], row["home_score"]
        if t1_goals > t2_goals:
            wins += 1
        goal_diffs.append(t1_goals - t2_goals)

    return {
        "team1_win_rate": wins / len(h2h),
        "avg_goal_diff": float(np.mean(goal_diffs)),
        "matches_found": len(h2h),
    }
