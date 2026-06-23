"""
manual_stats.py  (Portugal vs Uzbekistan -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, Group K, Matchday 2
Date/Time: Tuesday, June 23, 2026, 1:00pm ET / 6:00pm BST
Venue: Houston Stadium (NRG Stadium), Houston, Texas

Sources checked today: Al Jazeera, Sky Sports, ESPN, Opta Analyst, Goal.com,
RotoWire, Sports Illustrated, Sports Mole, Squawka, Racing Post, Yahoo Sports,
Houston Public Media, Fanorate (match reports, lineups, venue details)

CONTEXT GOING IN:
- These two nations have NEVER met before, at any level -- genuinely no
  head-to-head history to draw on. Uzbekistan are playing their first-ever
  World Cup match as a country.
- Portugal were held 1-1 by DR Congo on Matchday 1 (Joao Neves scored early,
  Yoane Wissa equalized) -- a flat performance; Ronaldo missed two clear
  chances set up by Conceicao and was largely peripheral. Portugal managed
  only 1 shot on target all game, drawing criticism for both the result
  and Ronaldo's place in the side.
- Uzbekistan lost 1-3 to Colombia on their World Cup debut. Abbosbek
  Fayzullaev scored their first-ever World Cup goal (60th minute), but
  they recorded zero touches in Colombia's box during the entire first
  half -- a historically poor attacking start before improving after halftime.
- Portugal's pre-tournament form (last 5): won 4, drew 1 -- beat Nigeria 2-1,
  Chile 2-1, the USA 2-0, drew 0-0 with Mexico, plus a 9-1 qualifying win
  over Armenia.
- Uzbekistan's recent form: lost 3 straight matches into the tournament,
  won just 2 of their last 8 prior to this World Cup.
- CONFLICTING REPORT: Uzbekistan's captain/creative midfielder Jaloliddin
  Masharipov is described as injured and a doubt by one source (Racing
  Post) but listed in the predicted XI by another (Goal.com/Yahoo). Flagged
  below with a reduced (not zero) start_prob to reflect genuine uncertainty
  rather than picking a side.
- Houston Stadium plays its roof permanently closed for the tournament,
  fully air-conditioned, with a temporary natural grass pitch (cool-season
  Kentucky bluegrass/perennial ryegrass mix grown in Colorado, shipped in,
  kept alive indoors under LED grow lights) -- conditions are mild/dry
  regardless of Houston's outside heat and humidity.

NOTE ON TEAM NAME: historical_data.py's dataset should match "Portugal"
and "Uzbekistan" directly.
"""

PORTUGAL = {
    # Pre-tournament form strong (4W-1D in last 5), but flat WC opener
    "win_rate": 0.65,
    "goals_for_avg": 2.0,
    "goals_against_avg": 0.8,
    "form_points_avg": 2.0,

    "players": [
        {"id": "Diogo Costa",            "start_prob": 0.9,  "events": []},
        {"id": "Diogo Dalot",            "start_prob": 0.85, "events": []},
        {
            "id": "Ruben Dias", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-17", "type": "rating", "value": 6.8},  # back from minor injury, started vs DR Congo
            ],
        },
        {"id": "Goncalo Inacio",         "start_prob": 0.6,  "events": []},
        {"id": "Tomas Araujo",           "start_prob": 0.5,  "events": []},
        {"id": "Nuno Mendes",            "start_prob": 0.85, "events": []},
        {"id": "Joao Cancelo",           "start_prob": 0.5,  "events": []},
        {
            "id": "Joao Neves", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-17", "type": "goal"},   # 6th-minute opener vs DR Congo
                {"date": "2026-06-17", "type": "rating", "value": 7.6},
            ],
        },
        {"id": "Vitinha",                "start_prob": 0.8,  "events": []},
        {
            "id": "Bruno Fernandes", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-17", "type": "rating", "value": 6.5},  # solid but not decisive vs DR Congo
            ],
        },
        {"id": "Bernardo Silva",         "start_prob": 0.55, "events": []},
        {
            "id": "Francisco Conceicao", "start_prob": 0.6,
            "events": [
                {"date": "2026-06-17", "type": "assist"},  # set up Ronaldo (twice, both missed) -- counted once
                {"date": "2026-06-17", "type": "rating", "value": 7.2},  # livelier than the player he may replace
            ],
        },
        {
            "id": "Cristiano Ronaldo", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-17", "type": "rating", "value": 5.3},  # peripheral, missed two clear chances
            ],
        },
        {"id": "Rafael Leao",            "start_prob": 0.55, "events": []},
        {"id": "Pedro Neto",             "start_prob": 0.5,  "events": []},
        {"id": "Joao Felix",             "start_prob": 0.35, "events": []},
        {"id": "Goncalo Ramos",          "start_prob": 0.2,  "events": []},
    ],

    # Indoor climate-controlled, mild/dry -- no real disruption either way
    "team_record_at_similar_conditions": 0.6,
}

UZBEKISTAN = {
    # Lost WC opener but a credible second-half showing; rough pre-tournament form
    "win_rate": 0.35,
    "goals_for_avg": 1.0,
    "goals_against_avg": 1.8,
    "form_points_avg": 1.0,

    "players": [
        {"id": "Utkir Yusupov",          "start_prob": 0.9,  "events": []},
        {"id": "Farrukh Sayfiev",        "start_prob": 0.7,  "events": []},
        {
            "id": "Rustam Ashurmatov", "start_prob": 0.55,
            "events": [
                {"date": "2026-06-17", "type": "injury_or_out"},  # calf issue, game-time decision for this match
            ],
        },
        {"id": "Khojiakbar Alijonov",    "start_prob": 0.5,  "events": []},
        {
            "id": "Abdukodir Khusanov", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-17", "type": "rating", "value": 6.6},  # composed despite a yellow card vs Colombia
            ],
        },
        {"id": "Odiljon Hamrobekov",     "start_prob": 0.75, "events": []},
        {"id": "Otabek Shukurov",        "start_prob": 0.75, "events": []},
        {
            "id": "Jaloliddin Masharipov", "start_prob": 0.4,  # CONFLICTING reports: injured per one source,
            "events": [],                                       # listed in predicted XI per another -- flagged, not resolved
        },
        {
            "id": "Abbosbek Fayzullaev", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-17", "type": "goal"},   # Uzbekistan's first-ever World Cup goal, vs Colombia
                {"date": "2026-06-17", "type": "rating", "value": 7.0},
            ],
        },
        {
            "id": "Eldor Shomurodov", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-17", "type": "rating", "value": 6.4},  # captain, led the line, 44 int'l goals/92 caps
            ],
        },
        {"id": "Oston Urunov",           "start_prob": 0.5,  "events": []},
        {"id": "Igor Sergeev",           "start_prob": 0.4,  "events": []},
        {"id": "Dostonbek Khamdamov",    "start_prob": 0.45, "events": []},
    ],

    # Mild/dry indoor venue is a notable departure from Central Asian
    # conditions Uzbekistan are more used to -- treated as a mild negative
    "team_record_at_similar_conditions": 0.4,
}

# No head-to-head data exists -- these nations have never played each other.
HEAD_TO_HEAD = {
    "team1_win_rate": 0.5,    # genuinely no data -- neutral default, not a guess
    "avg_goal_diff": 0.0,
}

VENUE = {
    "venue_name": "Houston Stadium (NRG Stadium), Houston, Texas",
    "pitch_type": "natural grass (84% Kentucky Bluegrass / 16% Perennial Ryegrass, "
                   "grown in Colorado, shipped in, maintained under LED grow lights)",
    "altitude_m": 13,
    "expected_conditions": "Roof permanently closed for the tournament, fully air-conditioned -- "
                            "mild and dry indoors regardless of Houston's outside heat/humidity "
                            "(90-95F, possible thunderstorms, outside the stadium)",
}

# No prior Portugal vs Uzbekistan matches exist (first-ever meeting) --
# nothing to backtest against for this fixture.
KNOWN_PAST_RESULTS = []