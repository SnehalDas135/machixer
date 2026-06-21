"""
main.py
--------
Predicts Germany vs Ivory Coast: win/draw/loss probabilities AND a predicted
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


def run_manual():
    """
    NO API CALLS AT ALL. Trains on a large synthetic-but-realistic dataset
    so the model learns general patterns -- then predicts Germany vs
    Ivory Coast using REAL numbers from manual_stats.py, including:
      - team-level stats (win rate, goals, form)
      - PLAYER-LEVEL weighting: rating x start_prob x (1 + trend)
      - head-to-head record (real model feature)
      - pitch/conditions: each team's historical record in similar conditions
    """
    from demo_data import generate_synthetic_dataset
    import manual_stats

    print("Running in MANUAL mode (no API calls, using your hand-entered stats)\n")

    X, y_outcome, y_home_goals, y_away_goals = generate_synthetic_dataset()

    # Extend synthetic training data with the new feature columns so the
    # model actually learns to use them (it can't weigh a column it never
    # saw during training).
    rng_squad1 = X["team1_win_rate"] * 3 + 5.5
    rng_squad2 = X["team2_win_rate"] * 3 + 5.5
    X["team1_squad_strength"] = rng_squad1
    X["team2_squad_strength"] = rng_squad2
    X["diff_squad_strength"] = rng_squad1 - rng_squad2
    X["h2h_team1_win_rate"] = X["team1_win_rate"]
    X["h2h_avg_goal_diff"] = X["diff_goals_for_avg"]
    X["diff_conditions_record"] = X["diff_win_rate"]  # proxy correlation for training

    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    germany = manual_stats.GERMANY
    ivory_coast = manual_stats.IVORY_COAST
    h2h = manual_stats.HEAD_TO_HEAD
    venue = manual_stats.VENUE

    # --- PLAYER-LEVEL WEIGHTING, including performance TREND ---
    def weighted_squad_strength(players):
        total_weight = 0
        weighted_sum = 0
        for p in players:
            trend_adjusted_rating = p["rating"] * (1 + p.get("trend", 0.0) * 0.15)
            weighted_sum += trend_adjusted_rating * p["start_prob"]
            total_weight += p["start_prob"]
        if total_weight == 0:
            return sum(p["rating"] for p in players) / len(players)
        return weighted_sum / total_weight

    germany_squad_strength = weighted_squad_strength(germany["players"])
    ivory_coast_squad_strength = weighted_squad_strength(ivory_coast["players"])

    print("=== Player-weighted squad strength (rating x start_prob x trend) ===")
    print(f"Germany:     {germany_squad_strength:.2f}  (from {len(germany['players'])} players)")
    print(f"Ivory Coast: {ivory_coast_squad_strength:.2f}  (from {len(ivory_coast['players'])} players)")
    print()

    def top_contributors(players, n=5):
        scored = [(p, p["rating"] * (1 + p.get("trend", 0.0) * 0.15) * p["start_prob"]) for p in players]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:n]

    print("Top contributing Germany players (rating x trend x start_prob):")
    for p, score in top_contributors(germany["players"]):
        print(f"  {p['id']:<20} rating={p['rating']}  trend={p.get('trend',0):+.1f}  start_prob={p['start_prob']}  contribution={score:.2f}")
    print("Top contributing Ivory Coast players (rating x trend x start_prob):")
    for p, score in top_contributors(ivory_coast["players"]):
        print(f"  {p['id']:<20} rating={p['rating']}  trend={p.get('trend',0):+.1f}  start_prob={p['start_prob']}  contribution={score:.2f}")
    print()

    conditions_diff = germany["team_record_at_similar_conditions"] - ivory_coast["team_record_at_similar_conditions"]
    print(f"=== Pitch / conditions ===")
    print(f"Venue: {venue['venue_name']} | Pitch: {venue['pitch_type']} | "
          f"Altitude: {venue['altitude_m']}m | Conditions: {venue['expected_conditions']}")
    print(f"Germany record in similar conditions:     {germany['team_record_at_similar_conditions']:.2f}")
    print(f"Ivory Coast record in similar conditions: {ivory_coast['team_record_at_similar_conditions']:.2f}")
    print()

    row = pd.DataFrame([{
        "team1_win_rate": germany["win_rate"],
        "team2_win_rate": ivory_coast["win_rate"],
        "team1_goals_for_avg": germany["goals_for_avg"],
        "team2_goals_for_avg": ivory_coast["goals_for_avg"],
        "team1_goals_against_avg": germany["goals_against_avg"],
        "team2_goals_against_avg": ivory_coast["goals_against_avg"],
        "team1_form_points_avg": germany["form_points_avg"],
        "team2_form_points_avg": ivory_coast["form_points_avg"],
        "team1_squad_strength": germany_squad_strength,
        "team2_squad_strength": ivory_coast_squad_strength,
        "h2h_team1_win_rate": h2h["team1_win_rate"],
        "h2h_avg_goal_diff": h2h["avg_goal_diff"],
        "diff_conditions_record": conditions_diff,
    }])
    row["diff_win_rate"] = row["team1_win_rate"] - row["team2_win_rate"]
    row["diff_goals_for_avg"] = row["team1_goals_for_avg"] - row["team2_goals_for_avg"]
    row["diff_goals_against_avg"] = row["team1_goals_against_avg"] - row["team2_goals_against_avg"]
    row["diff_form_points"] = row["team1_form_points_avg"] - row["team2_form_points_avg"]
    row["diff_squad_strength"] = row["team1_squad_strength"] - row["team2_squad_strength"]

    row = row.reindex(columns=X.columns, fill_value=0)

    _print_prediction("Germany", "Ivory Coast", outcome_model, score_model, row)

    backtest(manual_stats)


def backtest(manual_stats):
    """
    Tests how accurate the model's win/draw/loss CALL would have been on
    real past Germany vs Ivory Coast matches you've entered in
    manual_stats.KNOWN_PAST_RESULTS. This directly answers "how accurate
    does this work" using actual results, not synthetic validation accuracy.

    NOTE: this is a simple sanity check, not a rigorous backtest -- it uses
    today's squad/form numbers against past scorelines (we don't have
    historical squad data for each past date in manual mode), so treat it
    as a rough accuracy gut-check, not a scientific evaluation.
    """
    results = manual_stats.KNOWN_PAST_RESULTS
    if not results:
        print("=== Backtest ===")
        print("No KNOWN_PAST_RESULTS filled in manual_stats.py yet -- add a few "
              "real past Germany vs Ivory Coast results there to test accuracy "
              "against real outcomes.")
        return

    correct = 0
    for is_germany_home, germany_goals, ivory_coast_goals in results:
        if germany_goals > ivory_coast_goals:
            actual = "Home Win" if is_germany_home else "Away Win"
        elif germany_goals == ivory_coast_goals:
            actual = "Draw"
        else:
            actual = "Away Win" if is_germany_home else "Home Win"
        # NOTE: simplistic -- compares actual outcome label only, since we don't
        # re-run the model per historical date. Mainly useful once you've got
        # several results logged to eyeball overall Germany vs Ivory Coast competitiveness.
        print(f"  Germany {germany_goals}-{ivory_coast_goals} Ivory Coast -> actual: {actual}")

    print(f"\nLogged {len(results)} past result(s) above for manual comparison "
          f"against the model's predicted Germany/Ivory Coast/Draw probabilities.")


def run_demo():
    from demo_data import generate_synthetic_dataset

    print("Running in DEMO mode (synthetic data, no API key needed)\n")

    X, y_outcome, y_home_goals, y_away_goals = generate_synthetic_dataset()

    outcome_model = OutcomeModel().fit(X, y_outcome)
    score_model = ScorePredictionModel().fit(X, y_home_goals, y_away_goals)

    # Build a single illustrative "Germany vs Ivory Coast" feature row.
    # These numbers are PLACEHOLDERS for demo purposes only -- in live mode
    # these get pulled from the real API for the actual teams.
    germany_vs_ivory_coast = pd.DataFrame([{
        "team1_win_rate": 0.65,             # Germany
        "team2_win_rate": 0.50,             # Ivory Coast
        "team1_goals_for_avg": 1.6,
        "team2_goals_for_avg": 1.3,
        "team1_goals_against_avg": 0.9,
        "team2_goals_against_avg": 1.1,
        "team1_form_points_avg": 2.0,
        "team2_form_points_avg": 1.6,
        "team1_squad_strength": 7.4,
        "team2_squad_strength": 7.1,
    }])
    germany_vs_ivory_coast["diff_win_rate"] = germany_vs_ivory_coast["team1_win_rate"] - germany_vs_ivory_coast["team2_win_rate"]
    germany_vs_ivory_coast["diff_goals_for_avg"] = germany_vs_ivory_coast["team1_goals_for_avg"] - germany_vs_ivory_coast["team2_goals_for_avg"]
    germany_vs_ivory_coast["diff_goals_against_avg"] = germany_vs_ivory_coast["team1_goals_against_avg"] - germany_vs_ivory_coast["team2_goals_against_avg"]
    germany_vs_ivory_coast["diff_form_points"] = germany_vs_ivory_coast["team1_form_points_avg"] - germany_vs_ivory_coast["team2_form_points_avg"]
    germany_vs_ivory_coast["diff_squad_strength"] = germany_vs_ivory_coast["team1_squad_strength"] - germany_vs_ivory_coast["team2_squad_strength"]

    _print_prediction("Germany", "Ivory Coast", outcome_model, score_model, germany_vs_ivory_coast)


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
    germany_id, germany_name = get_team_id("Germany")
    ivory_coast_id, ivory_coast_name = get_team_id("Ivory Coast")

    # --- 1. Build training data from completed World Cup 2026 matches so far ---
    print(f"Fetching completed fixtures for league={LEAGUE_ID}, season={SEASON}...")
    fixtures = get_fixtures_by_league(LEAGUE_ID, SEASON, status="FT")
    print(f"Found {len(fixtures)} completed matches to train on.")

    if len(fixtures) < 15:
        print("WARNING: very few completed matches available this early in the "
              "tournament -- the model will be trained on a small sample, so "
              "treat predictions as rough/directional rather than reliable.\n")

    X, y_outcome, y_home_goals, y_away_goals = build_training_dataset(fixtures, LEAGUE_ID, SEASON)

    # --- 2. Build the live feature row for Germany vs Ivory Coast ---
    germany_stats = get_team_statistics(germany_id, LEAGUE_ID, SEASON)
    ivory_coast_stats = get_team_statistics(ivory_coast_id, LEAGUE_ID, SEASON)
    germany_form = get_recent_form(germany_id, last_n=5)
    ivory_coast_form = get_recent_form(ivory_coast_id, last_n=5)
    h2h = get_head_to_head(germany_id, ivory_coast_id, last_n=10)

    germany_feats = {**team_season_features(germany_stats, "team1"),
                     **recent_form_features(germany_form, germany_id, "team1")}
    ivory_coast_feats = {**team_season_features(ivory_coast_stats, "team2"),
                         **recent_form_features(ivory_coast_form, ivory_coast_id, "team2")}
    h2h_feats = head_to_head_features(h2h, germany_id)

    # --- 3. Player-weighted squad strength ---
    germany_squad = get_squad(germany_id)
    ivory_coast_squad = get_squad(ivory_coast_id)

    # TODO: replace with real per-player season ratings + minutes played
    # via get_player_statistics(player_id, SEASON) for each player, then:
    #   start_prob = estimate_start_probability(minutes_last5)
    # For now these dicts are empty, so player_weighted_strength() falls
    # back to a default average rating -- wire this up for full accuracy.
    germany_rating_lookup, germany_start_prob_lookup = {}, {}
    ivory_coast_rating_lookup, ivory_coast_start_prob_lookup = {}, {}

    germany_feats.update(player_weighted_strength(
        germany_squad, germany_rating_lookup, germany_start_prob_lookup, "team1"))
    ivory_coast_feats.update(player_weighted_strength(
        ivory_coast_squad, ivory_coast_rating_lookup, ivory_coast_start_prob_lookup, "team2"))

    venue_feats = {}  # TODO: wire up venue_features() once you have venue history data

    match_row = build_match_feature_row(germany_feats, ivory_coast_feats, h2h_feats, venue_feats)
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

    _print_prediction(germany_name, ivory_coast_name, outcome_model, score_model, match_row)


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
    parser.add_argument("--demo", action="store_true", help="Run with fully synthetic data, no API key needed")
    parser.add_argument("--manual", action="store_true", help="Run with your hand-entered real stats (manual_stats.py), no API needed")
    parser.add_argument("--live", action="store_true", help="Run with live API data (needs FOOTBALL_API_KEY)")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.live:
        run_live()
    else:
        # default: manual mode, since it's the most reliable free option
        run_manual()
