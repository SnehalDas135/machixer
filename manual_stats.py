"""
manual_stats.py  (Belgium vs Iran -- events-based, recency-weighted)
------------------------------------------------------------------------
Each player now holds REAL, DATED events (goals, assists, match ratings)
instead of a flat guessed rating. recency_scoring.py computes their actual
current-form score by decay-weighting these events -- a contribution from
last week counts far more than one from a year ago. I (the assistant)
supply the data; the code computes the weighting. That's the split you
asked for.

DATA COVERAGE -- BE HONEST ABOUT GAPS
----------------------------------------
Real dated events below were verified via search for: Kevin De Bruyne
(FotMob match ratings/goals/assists, dated), Mohammad Mohebi and Ramin
Rezaeian (each scored vs New Zealand on 2026-06-15, dated/sourced).

Every other player below has an EMPTY events list -- meaning I have NOT
yet verified real dated stats for them. Their score will fall back to a
neutral default (6.5) rather than a guessed number, and `real_data: False`
will print so the gap is visible, not hidden. Add real events for these
players the same way (date, type: goal/assist/rating/start/injury_or_out)
to replace the defaults with real computed scores. I can keep researching
more players if you want -- just say which ones to prioritize.

EVENT SCHEMA
--------------
  {"date": "YYYY-MM-DD", "type": "goal"}
  {"date": "YYYY-MM-DD", "type": "assist"}
  {"date": "YYYY-MM-DD", "type": "rating", "value": 7.6}   # actual match rating
  {"date": "YYYY-MM-DD", "type": "start"}                  # confirms fit/playing
  {"date": "YYYY-MM-DD", "type": "injury_or_out"}          # negative signal
"""

BELGIUM = {
    "win_rate": 0.60,
    "goals_for_avg": 2.0,
    "goals_against_avg": 0.6,
    "form_points_avg": 2.2,

    "players": [
        {"id": "Thibaut Courtois",      "start_prob": 0.95, "events": []},  # TODO: needs real events
        {"id": "Zeno Debast",           "start_prob": 0.8,  "events": []},
        {"id": "Koni De Winter",        "start_prob": 0.8,  "events": []},
        {"id": "Arthur Theate",         "start_prob": 0.75, "events": []},
        {"id": "Timothy Castagne",      "start_prob": 0.8,  "events": []},
        {"id": "Axel Witsel",           "start_prob": 0.7,  "events": []},
        {"id": "Youri Tielemans",       "start_prob": 0.85, "events": []},
        {
            "id": "Kevin De Bruyne", "start_prob": 0.9,
            # Real, dated, sourced via FotMob + match reports
            "events": [
                {"date": "2026-06-15", "type": "rating", "value": 6.5},  # Belgium 1-1 Egypt, WC opener
                {"date": "2026-04-24", "type": "rating", "value": 8.8},  # Napoli 4-0 Cremonese
                {"date": "2026-04-24", "type": "goal"},
                {"date": "2026-04-24", "type": "assist"},
                {"date": "2026-04-18", "type": "rating", "value": 6.1},  # Napoli 0-2 Lazio
                {"date": "2026-04-12", "type": "rating", "value": 7.6},  # Parma 1-1 Napoli
                {"date": "2026-04-06", "type": "rating", "value": 7.3},  # Napoli 1-0 Milan
            ],
        },
        {"id": "Jeremy Doku",           "start_prob": 0.85, "events": []},
        {"id": "Charles De Ketelaere",  "start_prob": 0.7,  "events": []},
        {"id": "Romelu Lukaku",         "start_prob": 0.6,  "events": []},  # impact sub vs Egypt -- needs dated event
    ],

    "team_record_at_similar_conditions": 0.55,
}

IRAN = {
    "win_rate": 0.55,
    "goals_for_avg": 1.7,
    "goals_against_avg": 1.1,
    "form_points_avg": 2.0,

    "players": [
        {"id": "Alireza Beiranvand",      "start_prob": 0.9,  "events": []},
        {"id": "Milad Mohammadi",         "start_prob": 0.85, "events": []},
        {"id": "Shoja Khalilzadeh",       "start_prob": 0.8,  "events": []},
        {"id": "Ali Nemati",              "start_prob": 0.75, "events": []},
        {
            "id": "Ramin Rezaeian", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-15", "type": "goal"},   # scored vs New Zealand, WC opener
            ],
        },
        {"id": "Saeid Ezatolahi",         "start_prob": 0.8,  "events": []},
        {"id": "Saman Ghoddos",           "start_prob": 0.8,  "events": []},
        {"id": "Mehdi Ghayedi",           "start_prob": 0.75, "events": []},
        {
            "id": "Mohammad Mohebi", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-15", "type": "goal"},   # 63rd-min equalizer vs New Zealand
            ],
        },
        {"id": "Mehdi Taremi",            "start_prob": 0.9,  "events": []},  # needs Olympiacos-season events
        {"id": "Shahriar Moghanlou",      "start_prob": 0.6,  "events": []},
    ],

    "team_record_at_similar_conditions": 0.48,
}

HEAD_TO_HEAD = {
    "team1_win_rate": 0.5,    # no head-to-head data found between these teams -- neutral default
    "avg_goal_diff": 0.0,
}

VENUE = {
    "venue_name": "Los Angeles Stadium (SoFi Stadium), Inglewood, California",
    "pitch_type": "natural grass (Kentucky bluegrass / perennial ryegrass cool-season mix, "
                   "grown on a modular tray system over the stadium's usual turf)",
    "altitude_m": 32,
    "expected_conditions": "Indoor, climate-controlled via translucent ETFE canopy with LED "
                            "grow lights -- mild and dry regardless of outside weather",
}

KNOWN_PAST_RESULTS = []  # no confirmed past Belgium vs Iran results found