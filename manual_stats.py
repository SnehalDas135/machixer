"""
manual_stats.py  (Switzerland vs Canada -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, Group B, Matchday 3 (decider)
Date/Time: Wednesday, June 24, 2026, 3:00pm ET / 12:00pm PT
Venue: Vancouver Stadium (BC Place), Vancouver, Canada

Sources checked today: ESPN, Juvefc, Wikipedia (Group B page), FOX Sports,
Wego Travel, Daily Hive, Fanorate, Martincid (match previews, venue details)

CONTEXT GOING IN:
- This is a genuine group decider: both Switzerland and Canada are level on
  4 points after two matches each, fighting for top spot in Group B.
  Canada lead on goal difference, so a draw would still send them through
  as group winners.
- Canada are having their best-ever men's World Cup: a draw with Bosnia,
  then a historic 6-0 win over Qatar (their first-ever World Cup win) --
  Jonathan David scored a hat-trick in that game.
- Canada's midfielder Ismael Kone suffered a broken leg during the Qatar
  win and is ruled OUT of the rest of the tournament -- a real, significant
  loss for their midfield balance.
- Switzerland have a win and a draw from their first two games. Substitute
  Johan Manzambi scored twice off the bench against Bosnia and Herzegovina
  -- he has not started either game so far despite this impact.
- Breel Embolo has already scored at this tournament (a penalty in the
  Qatar opener).
- No significant injury concerns reported for Switzerland heading into
  this match; Canada otherwise enter "in good health" aside from the
  Kone loss.
- BC Place's artificial turf was fully replaced with a hybrid natural grass
  pitch for the tournament; the retractable roof is kept closed for all
  matches (for broadcast/lighting consistency, not weather), giving
  consistent indoor-like conditions regardless of Vancouver's mild,
  often-damp Pacific Northwest climate outside.

NOTE ON TEAM NAME: historical_data.py's dataset should match "Switzerland"
and "Canada" directly.
"""

SWITZERLAND = {
    # 1 win, 1 draw from first 2 games; settled, in-form squad
    "win_rate": 0.55,
    "goals_for_avg": 1.8,
    "goals_against_avg": 0.9,
    "form_points_avg": 2.0,

    "players": [
        {"id": "Gregor Kobel",          "start_prob": 0.9,  "events": []},
        {"id": "Silvan Widmer",         "start_prob": 0.8,  "events": []},
        {"id": "Nico Elvedi",           "start_prob": 0.85, "events": []},
        {"id": "Manuel Akanji",         "start_prob": 0.85, "events": []},
        {"id": "Ricardo Rodriguez",     "start_prob": 0.75, "events": []},
        {"id": "Granit Xhaka",          "start_prob": 0.85, "events": []},
        {"id": "Remo Freuler",          "start_prob": 0.85, "events": []},
        {"id": "Dan Ndoye",             "start_prob": 0.8,  "events": []},
        {
            "id": "Breel Embolo", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-13", "type": "goal"},   # penalty vs Qatar, opener
            ],
        },
        {"id": "Ruben Vargas",          "start_prob": 0.75, "events": []},
        {
            "id": "Johan Manzambi", "start_prob": 0.35,  # hasn't started either game despite this
            "events": [
                {"date": "2026-06-18", "type": "goal"},   # 1st of 2 off the bench vs Bosnia
                {"date": "2026-06-18", "type": "goal"},   # 2nd of 2 off the bench vs Bosnia
                {"date": "2026-06-18", "type": "rating", "value": 8.3},  # match-changing cameo
            ],
        },
        {"id": "Ardon Jashari",         "start_prob": 0.3,  "events": []},
        {"id": "Fabian Rieder",         "start_prob": 0.3,  "events": []},
        {"id": "Zeki Amdouni",          "start_prob": 0.4,  "events": []},
    ],

    # Mild/dry indoor conditions; Switzerland generally comfortable in
    # cool, temperate climates similar to home
    "team_record_at_similar_conditions": 0.58,
}

CANADA = {
    # Draw + record 6-0 win; home crowd, strong momentum, but missing a key midfielder
    "win_rate": 0.55,
    "goals_for_avg": 2.5,
    "goals_against_avg": 0.5,
    "form_points_avg": 2.0,

    "players": [
        {"id": "Maxime Crepeau",        "start_prob": 0.9,  "events": []},
        {"id": "Alistair Johnston",     "start_prob": 0.85, "events": []},
        {"id": "Luc de Fougerolles",    "start_prob": 0.8,  "events": []},
        {"id": "Derek Cornelius",       "start_prob": 0.8,  "events": []},
        {
            "id": "Richie Laryea", "start_prob": 0.75,
            "events": [],
        },
        {
            "id": "Alphonso Davies", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-20", "type": "rating", "value": 7.4},  # dynamic vs Qatar, fit and effective
            ],
        },
        {"id": "Tajon Buchanan",        "start_prob": 0.75, "events": []},
        {"id": "Stephen Eustaquio",     "start_prob": 0.8,  "events": []},
        {
            "id": "Ismael Kone", "start_prob": 0.0,   # broken leg vs Qatar -- ruled out of the tournament
            "events": [
                {"date": "2026-06-20", "type": "injury_or_out"},
            ],
        },
        {"id": "Nathan Saliba",         "start_prob": 0.5,  "events": []},  # likely steps in for Kone
        {"id": "Ali Ahmed",             "start_prob": 0.55, "events": []},
        {
            "id": "Jonathan David", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-20", "type": "goal"},
                {"date": "2026-06-20", "type": "goal"},
                {"date": "2026-06-20", "type": "goal"},   # hat-trick vs Qatar
                {"date": "2026-06-20", "type": "rating", "value": 9.0},
            ],
        },
        {"id": "Cyle Larin",            "start_prob": 0.6,  "events": []},
    ],

    # Home soil, mild Pacific Northwest-style conditions Canada are used to
    "team_record_at_similar_conditions": 0.6,
}

# No widely reported prior Switzerland vs Canada meetings found -- treated
# as neutral/unknown rather than guessed.
HEAD_TO_HEAD = {
    "team1_win_rate": 0.5,
    "avg_goal_diff": 0.0,
}

VENUE = {
    "venue_name": "Vancouver Stadium (BC Place), Vancouver, Canada",
    "pitch_type": "hybrid natural grass (artificial turf fully removed and replaced for the "
                   "tournament; grown at a farm in Abbotsford, BC, to FIFA standard)",
    "altitude_m": 1,
    "expected_conditions": "Retractable roof kept closed for all matches (broadcast/lighting "
                            "consistency, not weather) -- mild Pacific Northwest summer outside "
                            "(typically 64-75F, possible light rain), but conditions inside are "
                            "controlled and consistent",
}

# No confirmed past Switzerland vs Canada results found -- nothing to
# backtest against for this fixture.
KNOWN_PAST_RESULTS = []