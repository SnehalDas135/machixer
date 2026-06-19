"""
demo_data.py
-------------
Generates a SYNTHETIC but statistically realistic dataset so you can run
the whole pipeline end-to-end right now, before plugging in a real API key.

This lets you verify the model code works (no bugs, no shape mismatches)
on your machine immediately. Once confirmed, swap demo_data.generate(...)
for training_data.build_training_dataset(...) using real fixtures.
"""

import numpy as np
import pandas as pd


def generate_synthetic_dataset(n_matches=1500, seed=42):
    rng = np.random.default_rng(seed)

    team1_win_rate = rng.uniform(0.2, 0.8, n_matches)
    team2_win_rate = rng.uniform(0.2, 0.8, n_matches)
    team1_goals_for_avg = rng.uniform(0.5, 2.5, n_matches)
    team2_goals_for_avg = rng.uniform(0.5, 2.5, n_matches)
    team1_goals_against_avg = rng.uniform(0.5, 2.0, n_matches)
    team2_goals_against_avg = rng.uniform(0.5, 2.0, n_matches)
    team1_form_points_avg = rng.uniform(0, 3, n_matches)
    team2_form_points_avg = rng.uniform(0, 3, n_matches)
    team1_squad_strength = rng.uniform(6.0, 8.5, n_matches)
    team2_squad_strength = rng.uniform(6.0, 8.5, n_matches)

    X = pd.DataFrame({
        "team1_win_rate": team1_win_rate,
        "team2_win_rate": team2_win_rate,
        "team1_goals_for_avg": team1_goals_for_avg,
        "team2_goals_for_avg": team2_goals_for_avg,
        "team1_goals_against_avg": team1_goals_against_avg,
        "team2_goals_against_avg": team2_goals_against_avg,
        "team1_form_points_avg": team1_form_points_avg,
        "team2_form_points_avg": team2_form_points_avg,
        "team1_squad_strength": team1_squad_strength,
        "team2_squad_strength": team2_squad_strength,
    })
    X["diff_win_rate"] = X["team1_win_rate"] - X["team2_win_rate"]
    X["diff_goals_for_avg"] = X["team1_goals_for_avg"] - X["team2_goals_for_avg"]
    X["diff_goals_against_avg"] = X["team1_goals_against_avg"] - X["team2_goals_against_avg"]
    X["diff_form_points"] = X["team1_form_points_avg"] - X["team2_form_points_avg"]
    X["diff_squad_strength"] = X["team1_squad_strength"] - X["team2_squad_strength"]

    # simulate "true" underlying strength -> expected goals -> actual goals (Poisson)
    lam_home = np.clip(1.3 + 0.6 * X["diff_win_rate"] + 0.3 * X["diff_squad_strength"], 0.2, 4)
    lam_away = np.clip(1.1 - 0.6 * X["diff_win_rate"] - 0.3 * X["diff_squad_strength"], 0.2, 4)

    y_home_goals = rng.poisson(lam_home)
    y_away_goals = rng.poisson(lam_away)

    y_outcome = np.where(y_home_goals > y_away_goals, 2,
                  np.where(y_home_goals == y_away_goals, 1, 0))

    return X, y_outcome, y_home_goals, y_away_goals
