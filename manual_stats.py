"""
manual_stats.py  (v3 -- player trends + pitch/conditions added)
------------------------------------------------------------------
NO API NEEDED. Fill these in by hand using free public sources:
- Wikipedia: "Netherlands national football team" / "Sweden national football team"
- https://www.transfermarkt.com   (squad list, market values, recent ratings)
- https://www.fbref.com           (player match-by-match ratings, free, no login)
- https://www.espn.com/soccer/    (recent form, probable lineups close to kickoff)
- Wikipedia: the specific stadium's page (pitch type, capacity, altitude,
  typical weather) plus that team's historical record at this venue/competition

WHAT THIS FILE COVERS (matches what you originally asked for)
------------------------------------------------------------------
  1. Team-level stats: win rate, goals for/against, recent form
  2. PLAYER-LEVEL: each key player's rating x start probability x recent
     performance TREND (not just a static guessed number)
  3. Head-to-head record: fed directly into the model
  4. PITCH / CONDITIONS: venue characteristics + how each team has
     historically performed in similar conditions

HOW TO FILL PLAYER LIST
--------------------------
  "rating"      : current form rating, 1-10 scale. 8.5+ = world-class/in
                  career-best form, 7-8 = strong starter, 6-7 = solid squad
                  player, below 6 = fringe/out of form.

  "start_prob"  : probability (0-1) they actually start. 1.0 = confirmed
                  starter. 0.7-0.9 = likely, healthy. 0.3-0.5 = rotation
                  risk/returning from injury. 0.0-0.2 = injured/suspended.

  "trend"       : performance TREND over their last 5 matches, -1.0 to +1.0.
                  Check their last 5 match ratings on FBref:
                  clearly improving (e.g. 6.5->7.0->7.8->8.0->8.3) = +1.0
                  flat/stable form = 0.0
                  clearly declining (e.g. 8.0->7.5->7.0->6.5->6.0) = -1.0
                  This is multiplied into their rating below, so a player on
                  a hot streak contributes MORE than their flat season
                  average would suggest; a player in a slump contributes less.

HOW TO FILL PITCH / CONDITIONS
---------------------------------
  "venue_name"        : the actual stadium name for this match
  "pitch_type"        : "natural grass", "hybrid grass", or "artificial turf"
                         (check the venue's Wikipedia page)
  "altitude_m"         : stadium's altitude in meters (affects stamina/ball
                         flight at high altitude -- check Wikipedia)
  "expected_conditions": short free-text, e.g. "hot and humid", "cold and
                         wet", "windy coastal venue" -- check recent weather
                         forecasts close to matchday for the real game.
  "team_record_at_similar_conditions" (per team): a 0-1 rough win rate this
       team has historically had in similar climate/altitude/pitch
       conditions (e.g. "Sweden in cold/wet conditions" vs "Sweden in
       hot/humid conditions" tend to differ -- look at past tournament
       results in similar host countries/climates for a reasonable estimate).
"""

NETHERLANDS = {
    "win_rate": 0.60,
    "goals_for_avg": 1.8,
    "goals_against_avg": 0.9,
    "form_points_avg": 2.2,

    # TODO: replace with the real ~11-15 key players + their real trend.
    "players": [
        {"id": "Bart Verbruggen",     "rating": 6.8, "start_prob": 0.9,  "trend": 0.0},
        {"id": "Virgil van Dijk",     "rating": 8.0, "start_prob": 1.0,  "trend": 0.2},
        {"id": "Jurrien Timber",      "rating": 7.5, "start_prob": 0.9,  "trend": 0.3},
        {"id": "Nathan Ake",          "rating": 7.2, "start_prob": 0.8,  "trend": 0.0},
        {"id": "Denzel Dumfries",     "rating": 7.6, "start_prob": 0.9,  "trend": 0.1},
        {"id": "Frenkie de Jong",     "rating": 8.0, "start_prob": 0.85, "trend": 0.4},
        {"id": "Tijjani Reijnders",   "rating": 7.4, "start_prob": 0.9,  "trend": 0.3},
        {"id": "Xavi Simons",         "rating": 7.8, "start_prob": 0.9,  "trend": 0.5},
        {"id": "Cody Gakpo",          "rating": 7.7, "start_prob": 0.9,  "trend": 0.2},
        {"id": "Memphis Depay",       "rating": 7.3, "start_prob": 0.6,  "trend": -0.2},
        {"id": "Donyell Malen",       "rating": 7.0, "start_prob": 0.7,  "trend": 0.1},
    ],

    "team_record_at_similar_conditions": 0.55,  # TODO
}

SWEDEN = {
    "win_rate": 0.40,
    "goals_for_avg": 1.3,
    "goals_against_avg": 1.2,
    "form_points_avg": 1.4,

    # TODO: replace with the real ~11-15 key players + their real trend.
    "players": [
        {"id": "Robin Olsen",         "rating": 6.5, "start_prob": 0.8,  "trend": 0.0},
        {"id": "Victor Lindelof",     "rating": 7.0, "start_prob": 0.9,  "trend": -0.1},
        {"id": "Emil Krafth",         "rating": 6.6, "start_prob": 0.8,  "trend": 0.0},
        {"id": "Gustav Isaksen",      "rating": 7.0, "start_prob": 0.8,  "trend": 0.2},
        {"id": "Alexander Isak",      "rating": 8.2, "start_prob": 0.85, "trend": 0.4},
        {"id": "Dejan Kulusevski",    "rating": 7.6, "start_prob": 0.85, "trend": 0.3},
        {"id": "Anthony Elanga",      "rating": 7.1, "start_prob": 0.8,  "trend": 0.2},
        {"id": "Albin Ekdal",         "rating": 6.7, "start_prob": 0.7,  "trend": -0.1},
        {"id": "Sander Berge",        "rating": 6.9, "start_prob": 0.7,  "trend": 0.0},
        {"id": "Viktor Gyokeres",     "rating": 7.9, "start_prob": 0.85, "trend": 0.3},
    ],

    "team_record_at_similar_conditions": 0.45,  # TODO
}

# Head-to-head: Netherlands' historical record specifically against Sweden.
HEAD_TO_HEAD = {
    "team1_win_rate": 0.55,   # TODO: Netherlands' win rate vs Sweden historically
    "avg_goal_diff": 0.4,     # TODO: Netherlands goals minus Sweden goals, averaged
}

# Pitch / venue / conditions for THIS specific match.
VENUE = {
    "venue_name": "TODO: fill in actual stadium",
    "pitch_type": "natural grass",        # TODO
    "altitude_m": 0,                       # TODO
    "expected_conditions": "TODO: e.g. mild and dry",
}

# A handful of REAL past matches for these two teams that you can look up,
# used to backtest/sanity-check the model's accuracy on data it can be
# checked against (see backtest() in main.py). Add as many as you can find
# (last 5-10 meetings or relevant matches is plenty).
# Format: (is_netherlands_home, netherlands_goals, sweden_goals)
KNOWN_PAST_RESULTS = [
    # TODO: fill in real historical Netherlands vs Sweden results, e.g.:
    # (True, 1, 1),   # Netherlands 1-1 Sweden (fill in real date/score)
    # (False, 0, 2),  # Sweden 2-0 Netherlands
]
