"""
main.py
--------
Predicts Morocco vs Scotland: win/draw/loss probabilities AND a predicted
final scoreline.

RUN MODES
=========
1. DEMO MODE (no API key needed) -- runs right now on synthetic data so you
   can confirm the pipeline works:
       python main.py --demo

2. LIVE MODE (real data, needs FOOTBALL_API_KEY env var set):
       python main.py

In live mode, you'll still need to fill in a couple of TODOs marked below --
mainly around pulling lineup/availability data, since "confirmed starting
lineup" usually isn't released until ~60 minutes before kickoff. Until then
we estimate start probability from recent minutes played.
"""

import argparse
import numpy as np
import pandas as pd

from model import OutcomeModel, ScorePredictionModel


OUTCOME_LABELS = {0: "Away Win", 1: "Draw", 2: "Home Win"}


def run_demo():
    from demo_data import generate_synthetic_dataset

    print("Running in DEMO mode (synthetic data, no API key needed)\n")

    X, y_outcome, y_home_goals, y_away_goals = generate_synthetic_dataset()

    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    # Build a single illustrative "Morocco vs Scotland" feature row.
    # These numbers are PLACEHOLDERS for demo purposes only -- in live mode
    # these get pulled from the real API for the actual teams.
    morocco_vs_scotland = pd.DataFrame([{
        "team1_win_rate": 0.55,             # Morocco
        "team2_win_rate": 0.45,             # Scotland
        "team1_goals_for_avg": 1.6,
        "team2_goals_for_avg": 1.3,
        "team1_goals_against_avg": 0.9,
        "team2_goals_against_avg": 1.1,
        "team1_form_points_avg": 2.0,
        "team2_form_points_avg": 1.6,
        "team1_squad_strength": 7.4,
        "team2_squad_strength": 7.1,
    }])
    morocco_vs_scotland["diff_win_rate"] = morocco_vs_scotland["team1_win_rate"] - morocco_vs_scotland["team2_win_rate"]
    morocco_vs_scotland["diff_goals_for_avg"] = morocco_vs_scotland["team1_goals_for_avg"] - morocco_vs_scotland["team2_goals_for_avg"]
    morocco_vs_scotland["diff_goals_against_avg"] = morocco_vs_scotland["team1_goals_against_avg"] - morocco_vs_scotland["team2_goals_against_avg"]
    morocco_vs_scotland["diff_form_points"] = morocco_vs_scotland["team1_form_points_avg"] - morocco_vs_scotland["team2_form_points_avg"]
    morocco_vs_scotland["diff_squad_strength"] = morocco_vs_scotland["team1_squad_strength"] - morocco_vs_scotland["team2_squad_strength"]

    _print_prediction("Morocco", "Scotland", outcome_model, score_model, morocco_vs_scotland)


def run_live():
    from data_fetcher import (
        get_team_id, get_team_statistics, get_recent_form,
        get_head_to_head, get_squad, get_player_statistics,
        get_fixtures_by_league,
    )
    from features import (
        team_season_features, recent_form_features, head_to_head_features,
        player_weighted_strength, estimate_start_probability,
        build_match_feature_row,
    )
    from training_data import build_training_dataset

    # FIFA World Cup 2026 = league id 1 on API-Football, confirmed via their
    # official docs (api-football.com/news/post/fifa-world-cup-2026-guide-to-using-data-with-api-sports)
    SEASON = 2026
    LEAGUE_ID = 1

    print("Fetching team IDs...")
    morocco_id, morocco_name = get_team_id("Morocco")
    scotland_id, scotland_name = get_team_id("Scotland")

    # --- 1. Build training data from completed World Cup 2026 matches so far ---
    print(f"Fetching completed fixtures for league={LEAGUE_ID}, season={SEASON}...")
    fixtures = get_fixtures_by_league(LEAGUE_ID, SEASON, status="FT")
    print(f"Found {len(fixtures)} completed matches to train on.")

    if len(fixtures) < 15:
        print("WARNING: very few completed matches available this early in the "
              "tournament -- the model will be trained on a small sample, so "
              "treat predictions as rough/directional rather than reliable.\n")

    X, y_outcome, y_home_goals, y_away_goals = build_training_dataset(fixtures, LEAGUE_ID, SEASON)

    # --- 2. Build the live feature row for Morocco vs Scotland ---
    morocco_stats = get_team_statistics(morocco_id, LEAGUE_ID, SEASON)
    scotland_stats = get_team_statistics(scotland_id, LEAGUE_ID, SEASON)
    morocco_form = get_recent_form(morocco_id, last_n=5)
    scotland_form = get_recent_form(scotland_id, last_n=5)
    h2h = get_head_to_head(morocco_id, scotland_id, last_n=10)

    morocco_feats = {**team_season_features(morocco_stats, "team1"),
                      **recent_form_features(morocco_form, morocco_id, "team1")}
    scotland_feats = {**team_season_features(scotland_stats, "team2"),
                       **recent_form_features(scotland_form, scotland_id, "team2")}
    h2h_feats = head_to_head_features(h2h, morocco_id)

    # --- 3. Player-weighted squad strength ---
    morocco_squad = get_squad(morocco_id)
    scotland_squad = get_squad(scotland_id)

    # TODO: replace with real per-player season ratings + minutes played
    # via get_player_statistics(player_id, SEASON) for each player, then:
    #   start_prob = estimate_start_probability(minutes_last5)
    # For now these dicts are empty, so player_weighted_strength() falls
    # back to a default average rating -- wire this up for full accuracy.
    morocco_rating_lookup, morocco_start_prob_lookup = {}, {}
    scotland_rating_lookup, scotland_start_prob_lookup = {}, {}

    morocco_feats.update(player_weighted_strength(
        morocco_squad, morocco_rating_lookup, morocco_start_prob_lookup, "team1"))
    scotland_feats.update(player_weighted_strength(
        scotland_squad, scotland_rating_lookup, scotland_start_prob_lookup, "team2"))

    venue_feats = {}  # TODO: wire up venue_features() once you have venue history data

    match_row = build_match_feature_row(morocco_feats, scotland_feats, h2h_feats, venue_feats)
    match_row = match_row.fillna(0)

    # --- 4. Train the models on real historical data, then predict ---
    if len(X) < 10:
        print("\nNot enough completed matches yet to train a meaningful model "
              "(need at least ~10-15). Try again closer to/during the tournament "
              "once more matches have been played, or run --demo to test mechanics.")
        return

    print("\nTraining models on real historical fixtures...")
    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    # match_row's columns must match what the models were trained on
    match_row = match_row.reindex(columns=X.columns, fill_value=0)

    _print_prediction(morocco_name, scotland_name, outcome_model, score_model, match_row)


def _print_prediction(team1_name, team2_name, outcome_model, score_model, feature_row):
    probs = outcome_model.predict_proba(feature_row)
    lam1, lam2 = score_model.predict_expected_goals(feature_row)
    most_likely, top5 = score_model.simulate_scoreline(lam1, lam2)

    print(f"\n=== {team1_name} vs {team2_name} Prediction ===")
    print(f"{team1_name} win probability:  {probs['home_win']*100:.1f}%")
    print(f"Draw probability:              {probs['draw']*100:.1f}%")
    print(f"{team2_name} win probability:  {probs['away_win']*100:.1f}%")
    print(f"\nExpected goals -> {team1_name}: {lam1:.2f}  |  {team2_name}: {lam2:.2f}")
    print(f"Most likely scoreline: {team1_name} {most_likely['score'].replace('-', f' - ')} {team2_name}  "
          f"({most_likely['probability']*100:.1f}% chance)")
    print("\nTop 5 most probable scorelines:")
    for s in top5:
        print(f"  {team1_name} {s['score']} {team2_name}  -- {s['probability']*100:.1f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run with synthetic data, no API key needed")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_live()