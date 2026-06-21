"""
main.py  (Belgium vs Iran)
------------------------------------
Predicts Belgium vs Iran: win/draw/loss probabilities AND a
predicted final scoreline.

RUN MODES
=========
1. REAL MODE (default, recommended) -- trains on ~49,000 real international
   match results (free CSV, no API key, no signup) and pulls Belgium's and
   Iran's actual current form + head-to-head automatically:
       python3 main.py

2. DEMO MODE -- fully synthetic data, no internet needed at all, just to
   sanity-check the code runs:
       python3 main.py --demo

Player-level weighting (rating x start_prob x trend) and pitch/conditions
come from manual_stats.py either way, since no free dataset has that level
of detail -- fill in the TODOs there with real current squad info.
"""

import argparse
import numpy as np
import pandas as pd

from model import OutcomeModel, ScorePredictionModel

OUTCOME_LABELS = {0: "Away Win", 1: "Draw", 2: "Home Win"}


def run_real():
    """
    Trains on real historical match data (1872-2024, free CSV from GitHub)
    instead of synthetic data -- this is what actually gives the model real
    predictive signal rather than near-random accuracy.

    Team-level stats (win rate, goals, form) AND head-to-head are computed
    automatically from real match history. Player-level scores are computed
    by recency_scoring.py from real dated events (goals/assists/ratings),
    not hand-assigned -- see manual_stats.py for data coverage notes.
    """
    import historical_data
    import manual_stats
    from recency_scoring import compute_squad_strength

    TEAM1, TEAM2 = "Belgium", "Iran"

    print(f"Loading real historical match data for {TEAM1} vs {TEAM2}...")
    df = historical_data.load_results(min_year=2005)
    print(f"Loaded {len(df)} real matches.\n")

    print("Building leakage-safe training features from real match history...")
    X, y_outcome, y_home_goals, y_away_goals = historical_data.build_training_dataset(df)
    print(f"Training on {len(X)} real matches.\n")

    t1_stats = historical_data.get_current_team_stats(df, TEAM1)
    t2_stats = historical_data.get_current_team_stats(df, TEAM2)
    h2h = historical_data.get_head_to_head(df, TEAM1, TEAM2)

    print(f"{TEAM1} real recent form (last {t1_stats['matches_used']} matches, "
          f"through {t1_stats['last_match_date'].date()}): "
          f"win_rate={t1_stats['win_rate']:.2f}, goals_for={t1_stats['goals_for_avg']:.2f}, "
          f"goals_against={t1_stats['goals_against_avg']:.2f}, form={t1_stats['form_points_avg']:.2f}")
    print(f"{TEAM2} real recent form (last {t2_stats['matches_used']} matches, "
          f"through {t2_stats['last_match_date'].date()}): "
          f"win_rate={t2_stats['win_rate']:.2f}, goals_for={t2_stats['goals_for_avg']:.2f}, "
          f"goals_against={t2_stats['goals_against_avg']:.2f}, form={t2_stats['form_points_avg']:.2f}")

    if h2h["matches_found"] > 0:
        print(f"Real head-to-head (last {h2h['matches_found']} meetings): "
              f"{TEAM1} win rate={h2h['team1_win_rate']:.2f}, avg goal diff={h2h['avg_goal_diff']:.2f}\n")
    else:
        print(f"No direct head-to-head matches found in the dataset between {TEAM1} and {TEAM2} "
              f"-- using neutral defaults (0.5 win rate, 0 goal diff).\n")

    g = manual_stats.BELGIUM
    ic = manual_stats.IRAN
    venue = manual_stats.VENUE

    t1_squad_strength, t1_breakdown = compute_squad_strength(g["players"])
    t2_squad_strength, t2_breakdown = compute_squad_strength(ic["players"])
    print(f"Player-weighted squad strength -> {TEAM1}: {t1_squad_strength:.2f}, {TEAM2}: {t2_squad_strength:.2f}\n")

    def _print_breakdown(team_name, breakdown):
        print(f"{team_name} player scores (computed from real dated events where available):")
        for b in sorted(breakdown, key=lambda x: x["contribution"], reverse=True):
            tag = "real data" if b["real_data"] else "DEFAULT (no events logged yet)"
            print(f"  {b['id']:<22} score={b['computed_score']:.2f}  start_prob={b['start_prob']}  "
                  f"contribution={b['contribution']:.2f}  [{tag}]")

    _print_breakdown(TEAM1, t1_breakdown)
    _print_breakdown(TEAM2, t2_breakdown)
    print()

    # Add squad_strength + h2h as training columns too -- the real dataset
    # doesn't have historical squad-strength data, so we proxy it with a
    # signal correlated to real win_rate just so the model has *some* learned
    # relationship for these columns; treat it as a secondary signal layered
    # on top of the real team-stat signal, not the main driver of the result.
    X = X.copy()
    X["team1_squad_strength"] = X["diff_win_rate"] * 2 + 7.0
    X["team2_squad_strength"] = 7.0 - X["diff_win_rate"] * 2
    X["diff_squad_strength"] = X["team1_squad_strength"] - X["team2_squad_strength"]
    X["h2h_team1_win_rate"] = X["diff_win_rate"].clip(0, 1)
    X["h2h_avg_goal_diff"] = X["diff_goals_for_avg"]

    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    h2h_win_rate = h2h["team1_win_rate"] if h2h["matches_found"] > 0 else 0.5
    h2h_goal_diff = h2h["avg_goal_diff"] if h2h["matches_found"] > 0 else 0.0

    row = pd.DataFrame([{
        "team1_win_rate": t1_stats["win_rate"],
        "team2_win_rate": t2_stats["win_rate"],
        "team1_goals_for_avg": t1_stats["goals_for_avg"],
        "team2_goals_for_avg": t2_stats["goals_for_avg"],
        "team1_goals_against_avg": t1_stats["goals_against_avg"],
        "team2_goals_against_avg": t2_stats["goals_against_avg"],
        "team1_form_points_avg": t1_stats["form_points_avg"],
        "team2_form_points_avg": t2_stats["form_points_avg"],
        "team1_squad_strength": t1_squad_strength,
        "team2_squad_strength": t2_squad_strength,
        "h2h_team1_win_rate": h2h_win_rate,
        "h2h_avg_goal_diff": h2h_goal_diff,
    }])
    row["diff_win_rate"] = row["team1_win_rate"] - row["team2_win_rate"]
    row["diff_goals_for_avg"] = row["team1_goals_for_avg"] - row["team2_goals_for_avg"]
    row["diff_goals_against_avg"] = row["team1_goals_against_avg"] - row["team2_goals_against_avg"]
    row["diff_form_points"] = row["team1_form_points_avg"] - row["team2_form_points_avg"]
    row["diff_squad_strength"] = row["team1_squad_strength"] - row["team2_squad_strength"]
    row = row.reindex(columns=X.columns, fill_value=0)

    print(f"Venue: {venue['venue_name']} | Pitch: {venue['pitch_type']} | Conditions: {venue['expected_conditions']}\n")

    _print_prediction(TEAM1, TEAM2, outcome_model, score_model, row)
    _backtest(manual_stats, TEAM1, TEAM2)


def _backtest(manual_stats, team1_name, team2_name):
    results = manual_stats.KNOWN_PAST_RESULTS
    if not results:
        print("=== Backtest ===")
        print(f"No KNOWN_PAST_RESULTS filled in manual_stats.py -- add a few real past "
              f"{team1_name} vs {team2_name} results there to sanity-check against the prediction.")
        return

    print("=== Backtest (real past results, for sanity-checking) ===")
    for is_t1_home, t1_goals, t2_goals in results:
        if t1_goals > t2_goals:
            actual = "Home Win" if is_t1_home else "Away Win"
        elif t1_goals == t2_goals:
            actual = "Draw"
        else:
            actual = "Away Win" if is_t1_home else "Home Win"
        print(f"  {team1_name} {t1_goals}-{t2_goals} {team2_name} -> actual: {actual}")


def run_demo():
    """Fully synthetic data, no internet needed -- just confirms the code runs."""
    from demo_data import generate_synthetic_dataset

    print("Running in DEMO mode (synthetic data, no internet needed)\n")

    X, y_outcome, y_home_goals, y_away_goals = generate_synthetic_dataset()
    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    belgium_vs_iran = pd.DataFrame([{
        "team1_win_rate": 0.60,             # Belgium (placeholder for demo only)
        "team2_win_rate": 0.55,             # Iran
        "team1_goals_for_avg": 2.0,
        "team2_goals_for_avg": 1.7,
        "team1_goals_against_avg": 0.6,
        "team2_goals_against_avg": 1.1,
        "team1_form_points_avg": 2.2,
        "team2_form_points_avg": 2.0,
        "team1_squad_strength": 7.6,
        "team2_squad_strength": 7.0,
    }])
    belgium_vs_iran["diff_win_rate"] = belgium_vs_iran["team1_win_rate"] - belgium_vs_iran["team2_win_rate"]
    belgium_vs_iran["diff_goals_for_avg"] = belgium_vs_iran["team1_goals_for_avg"] - belgium_vs_iran["team2_goals_for_avg"]
    belgium_vs_iran["diff_goals_against_avg"] = belgium_vs_iran["team1_goals_against_avg"] - belgium_vs_iran["team2_goals_against_avg"]
    belgium_vs_iran["diff_form_points"] = belgium_vs_iran["team1_form_points_avg"] - belgium_vs_iran["team2_form_points_avg"]
    belgium_vs_iran["diff_squad_strength"] = belgium_vs_iran["team1_squad_strength"] - belgium_vs_iran["team2_squad_strength"]

    _print_prediction("Belgium", "Iran", outcome_model, score_model, belgium_vs_iran)


def _print_prediction(team1_name, team2_name, outcome_model, score_model, feature_row):
    probs = outcome_model.predict_proba(feature_row)
    lam1, lam2 = score_model.predict_expected_goals(feature_row)
    most_likely, top5 = score_model.simulate_scoreline(lam1, lam2)

    print(f"\n=== {team1_name} vs {team2_name} Prediction ===")
    print(f"{team1_name} win probability:  {probs['home_win']*100:.1f}%")
    print(f"Draw probability:              {probs['draw']*100:.1f}%")
    print(f"{team2_name} win probability:  {probs['away_win']*100:.1f}%")
    print(f"\nExpected goals -> {team1_name}: {lam1:.2f}  |  {team2_name}: {lam2:.2f}")
    print(f"Most likely scoreline: {team1_name} {most_likely['score'].replace('-', ' - ')} {team2_name}  "
          f"({most_likely['probability']*100:.1f}% chance)")
    print("\nTop 5 most probable scorelines:")
    for s in top5:
        print(f"  {team1_name} {s['score']} {team2_name}  -- {s['probability']*100:.1f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run with fully synthetic data, no internet needed")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_real()