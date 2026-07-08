"""
recency_scoring.py
--------------------
This is the actual "model decides the weighting" piece you asked for.

Instead of me assigning a flat 1-10 rating per player, each player holds a
list of REAL, DATED events (goals, assists, match ratings, appearances).
This module computes their current form score by decay-weighting those
events by recency -- a contribution from last week counts far more than
one from a year ago, exactly like you described (1 goal a year ago should
count for much less than 1 goal last game).

THE DATA (events) comes from research. THE WEIGHTING (this code) is the model.

HOW THE DECAY WORKS
----------------------
weight(days_ago) = 0.5 ** (days_ago / half_life_days)

With half_life_days=180 (~6 months):
  - an event today:        weight = 1.00
  - an event 6 months ago: weight = 0.50
  - an event 1 year ago:   weight = 0.25
  - an event 2 years ago:  weight = 0.0625

A player's score = the weighted average of their event values, using these
weights -- so someone in current hot form (recent goals/high ratings)
scores higher than someone whose only evidence is old, even if their
career totals look similar on paper.

EVENT VALUES (what each event type is worth, before decay)
--------------------------------------------------------------
  "goal"        : 3.0   (scoring is the strongest positive signal)
  "assist"      : 2.0
  "rating"      : the actual match rating itself (e.g. FotMob/Sofascore,
                   typically 1-10) -- used directly as the event value
  "start"       : 1.0   (just confirms they're playing/fit, weak signal alone)
  "injury_or_out": -5.0 (strong negative signal, e.g. "ruled out", "injured")

These weights (3.0, 2.0, etc.) are a reasonable, transparent starting
scheme -- not hidden, not "trust me." You can change them in EVENT_VALUES
below and every player's score recomputes automatically.
"""

from datetime import datetime
import numpy as np

EVENT_VALUES = {
    "goal": 1.5,
    "assist": 1.0,
    "start": 0.2,
    "injury_or_out": -3.0,
    # "rating" events don't use this dict -- see compute_player_score,
    # where the rating's distance from the baseline (6.5) is used instead
}


def _days_ago(event_date_str, as_of):
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
    return (as_of - event_date).days


def compute_player_score(events, as_of=None, half_life_days=180, default_score=6.5):
    """
    events: list of dicts like:
        {"date": "2026-04-24", "type": "rating", "value": 8.8}
        {"date": "2026-06-15", "type": "goal"}
        {"date": "2025-10-25", "type": "injury_or_out"}

    Returns a single recency-weighted current-form score, computed as a
    BASELINE plus a recency-weighted adjustment from events -- not the raw
    average of event values. This matters: a single real "goal" event
    averaged alone would equal 3.0, which looks worse than a player with
    zero data (default 6.5) -- clearly wrong, since scoring a goal should
    raise your score, not lower it. Instead, each event nudges the score
    up/down from the baseline, decayed by recency.

    If a player has no events logged yet (data not gathered), returns
    default_score and flags it so you know it's a placeholder, not a real
    computed number.
    """
    if as_of is None:
        as_of = datetime.now()

    if not events:
        return default_score, False  # False = not real data, just a fallback

    weighted_adjustment = 0.0
    total_weight = 0.0
    for e in events:
        days = max(_days_ago(e["date"], as_of), 0)
        w = 0.5 ** (days / half_life_days)
        if e["type"] == "rating":
            adjustment = e["value"] - default_score  # how far above/below baseline this match was
        else:
            adjustment = EVENT_VALUES.get(e["type"], 0.0)
        weighted_adjustment += adjustment * w
        total_weight += w

    if total_weight == 0:
        return default_score, False

    avg_adjustment = weighted_adjustment / total_weight
    score = default_score + avg_adjustment
    return score, True  # True = real, computed from actual dated events


def compute_squad_strength(players, as_of=None, half_life_days=180):
    """
    players: list of dicts like:
        {"id": "Kevin De Bruyne", "start_prob": 0.9, "events": [...]}

    Computes each player's recency-weighted score from their events, then
    combines into squad strength weighted by start probability -- so a
    player in great current form who's NOT starting contributes little,
    and a player in good form who IS starting contributes a lot.

    Returns (squad_strength, per_player_breakdown) where breakdown lets you
    see exactly which players are running on real computed data vs a
    default placeholder (so gaps are visible, not hidden).
    """
    total_weight = 0.0
    weighted_sum = 0.0
    breakdown = []

    for p in players:
        score, is_real = compute_player_score(p.get("events", []), as_of, half_life_days)
        contribution = score * p["start_prob"]
        weighted_sum += contribution
        total_weight += p["start_prob"]
        breakdown.append({
            "id": p["id"],
            "computed_score": round(score, 2),
            "start_prob": p["start_prob"],
            "contributin": round(contribution, 2),
            "real_data": is_real,
        })

    squad_strength = weighted_sum / total_weight if total_weight else 6.5
    return squad_strength, breakdown