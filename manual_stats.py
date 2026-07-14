"""
manual_stats.py  (France vs Spain -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, Semi-final (Match 101)
Date/Time: Tuesday, July 14, 2026, 2:00pm ET / 19:00 GMT (Bastille Day)
Venue: Dallas Stadium (AT&T Stadium), Arlington, Texas

Sources checked: Al Jazeera, Sports Mole (previews + team news), Yahoo
Sports, FIFA.com, ESPN (match previews, squad news, tournament recaps)

CONTEXT GOING IN:
- The two pre-tournament favourites and highest-ranked European sides
  meet in the first semifinal. France have been the tournament's most
  dangerous attack (16 goals scored, the most of any team, with an
  attacking trio of Mbappe/Dembele/Olise combining for the bulk of it);
  Spain have been its most miserly defence, having conceded ZERO goals
  across all 6 games so far (Cape Verde 0-0, Saudi Arabia 4-0, Uruguay
  1-0, Austria 3-0, Portugal 1-0, Belgium 1-0). France are unbeaten too,
  winning all 6 of their games (Senegal 3-1, Iraq 3-0, Norway 4-1, Sweden
  3-0, Paraguay 1-0, Morocco 2-0).
- Kylian Mbappe leads the Golden Boot race with 8 goals (his 20th World
  Cup goal in as many career appearances). He picked up a minor ankle
  knock late in the Morocco win but said afterward he was "completely
  fine" and is expected to start as normal.
- France have two other fitness situations being monitored, both expected
  to be fine: Aurelien Tchouameni (thigh issue, has returned to full
  training) and Manu Kone (minor knee knock, came off vs Morocco but
  expected available). Saliba and Upamecano both missed a Saturday
  training session (rest day / individual session respectively) but are
  also expected to be fine to start.
- Spain have a near-fully-fit squad. The only doubt is winger Victor
  Munoz. Nico Williams and Yeremy Pino have recovered from mid-tournament
  injuries but are expected to stay on the bench. Mikel Merino has come
  off the bench in each of Spain's last two knockout games (Round of 16
  vs Portugal, Quarterfinal vs Belgium) and scored the winning goal both
  times, but is expected to remain an impact substitute rather than start.
  Mikel Oyarzabal has 4 tournament goals and is an outside shout for the
  Golden Boot; Lamine Yamal did not start the opener (not fully fit yet)
  but has started every game since.
- Historically, the sides have met 38 times overall, with Spain winning 7
  of the last 10 meetings -- including the two most recent and highest-
  profile: a 2-1 Spain win in the Euro 2024 semifinal (Yamal and Dani Olmo
  scoring) and a wild 5-4 Spain win (after extra time) in the 2025 UEFA
  Nations League semifinal (Yamal brace, Merino also scoring; Mbappe
  scored a penalty for France). Their only prior meeting at a World Cup
  was the 2006 Round of 16, which France won 3-1 (Franck Ribery, Patrick
  Vieira, and Zinedine Zidane scoring).
- Dallas Stadium (AT&T Stadium) is a retractable-roof stadium; expect
  fully controlled indoor conditions for this match.

NOTE ON TEAM NAME: historical_data.py's dataset should match "France"
and "Spain" directly.
"""

FRANCE = {
    # Perfect 6-0-0 record, the tournament's top scorers (16 goals) --
    # unbeaten through group stage, R32, R16, and the QF
    "win_rate": 1.0,
    "goals_for_avg": 2.67,       # 16 goals / 6 games
    "goals_against_avg": 0.33,   # 2 goals against / 6 games
    "form_points_avg": 3.0,

    "players": [
        {"id": "Mike Maignan",          "start_prob": 0.95, "events": []},
        {"id": "Jules Kounde",          "start_prob": 0.9,  "events": []},
        {
            "id": "William Saliba", "start_prob": 0.85,   # missed Saturday training (rest day), expected fine
            "events": [],
        },
        {
            "id": "Dayot Upamecano", "start_prob": 0.85,   # missed Saturday training (individual session), expected fine
            "events": [],
        },
        {"id": "Lucas Digne",           "start_prob": 0.85, "events": []},
        {
            "id": "Manu Kone", "start_prob": 0.65,   # minor knee knock vs Morocco, expected available
            "events": [
                {"date": "2026-07-11", "type": "injury_or_out"},   # came off with knee knock, downgraded severity
            ],
        },
        {
            "id": "Adrien Rabiot", "start_prob": 0.85,
            "events": [],
        },
        {
            "id": "Aurelien Tchouameni", "start_prob": 0.5,   # thigh issue, back in full training
            "events": [
                {"date": "2026-07-01", "type": "injury_or_out"},   # sustained after R32 win over Sweden
            ],
        },
        {
            "id": "Ousmane Dembele", "start_prob": 0.9,   # reigning Ballon d'Or winner
            "events": [
                {"date": "2026-06-27", "type": "goal"},   # hat-trick vs Norway, group finale
                {"date": "2026-06-27", "type": "goal"},
                {"date": "2026-06-27", "type": "goal"},
                {"date": "2026-07-11", "type": "rating", "value": 8.2},
            ],
        },
        {
            "id": "Michael Olise", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-11", "type": "rating", "value": 7.8},
            ],
        },
        {
            "id": "Kylian Mbappe", "start_prob": 0.9,   # captain; minor ankle knock but "completely fine"
            "events": [
                {"date": "2026-06-16", "type": "goal"},
                {"date": "2026-06-21", "type": "goal"},
                {"date": "2026-06-27", "type": "goal"},
                {"date": "2026-07-01", "type": "goal"},
                {"date": "2026-07-05", "type": "goal"},
                {"date": "2026-07-11", "type": "goal"},   # 8th goal, vs Morocco QF; ankle knock late on
                {"date": "2026-07-11", "type": "rating", "value": 8.4},
            ],
        },
        {"id": "Desire Doue",           "start_prob": 0.5,  "events": []},   # rotates on the left with Barcola
        {"id": "Bradley Barcola",       "start_prob": 0.5,  "events": []},   # rotates on the left with Doue
    ],

    "team_record_at_similar_conditions": 0.65,
}

SPAIN = {
    # 5 wins, 1 draw, 0 losses; the tournament's best defensive record --
    # yet to concede a single goal across 6 games
    "win_rate": 0.83,
    "goals_for_avg": 1.67,       # 10 goals / 6 games
    "goals_against_avg": 0.0,    # 0 goals against / 6 games -- untouched all tournament
    "form_points_avg": 2.67,

    "players": [
        {
            "id": "Unai Simon", "start_prob": 0.95,
            "events": [
                {"date": "2026-07-11", "type": "rating", "value": 8.2},  # extended the record clean-sheet run
            ],
        },
        {"id": "Pedro Porro",           "start_prob": 0.8,  "events": []},   # won the RB job over Llorente
        {"id": "Pau Cubarsi",           "start_prob": 0.85, "events": []},
        {"id": "Aymeric Laporte",       "start_prob": 0.85, "events": []},
        {"id": "Marc Cucurella",        "start_prob": 0.85, "events": []},
        {
            "id": "Rodri", "start_prob": 0.9,   # captain, midfield anchor
            "events": [],
        },
        {"id": "Fabian Ruiz",           "start_prob": 0.55, "events": []},   # rotating with Pedri
        {
            "id": "Dani Olmo", "start_prob": 0.85,   # attacking midfield
            "events": [],
        },
        {
            "id": "Lamine Yamal", "start_prob": 0.85,   # didn't start opener (unfit), has started every game since
            "events": [
                {"date": "2026-06-21", "type": "goal"},
                {"date": "2026-07-11", "type": "rating", "value": 8.0},
            ],
        },
        {
            "id": "Alex Baena", "start_prob": 0.6,   # won the starting job over Ferran Torres
            "events": [
                {"date": "2026-06-26", "type": "assist"},
            ],
        },
        {
            "id": "Mikel Oyarzabal", "start_prob": 0.85,   # 4 tournament goals, outside Golden Boot shout
            "events": [
                {"date": "2026-06-15", "type": "goal"},
                {"date": "2026-06-21", "type": "goal"},
                {"date": "2026-06-26", "type": "goal"},
                {"date": "2026-07-02", "type": "goal"},
                {"date": "2026-07-11", "type": "rating", "value": 7.7},
            ],
        },
        {
            "id": "Mikel Merino", "start_prob": 0.35,   # impact sub, winning goal in each of last 2 knockout games
            "events": [
                {"date": "2026-07-06", "type": "goal"},   # winner vs Portugal, R16
                {"date": "2026-07-11", "type": "goal"},   # winner vs Belgium, QF
                {"date": "2026-07-11", "type": "rating", "value": 8.3},
            ],
        },
        {"id": "Pedri",                 "start_prob": 0.4,  "events": []},   # rotated out for Fabian Ruiz recently
        {
            "id": "Victor Munoz", "start_prob": 0.4,   # fitness doubt for this match
            "events": [
                {"date": "2026-07-13", "type": "injury_or_out"},
            ],
        },
    ],

    "team_record_at_similar_conditions": 0.6,
}

# Real head-to-head record found: 38 all-time meetings, Spain winning 7 of
# the last 10. Both of the two most recent, most notable meetings were
# Spain wins: Euro 2024 semifinal (2-1) and the 2025 Nations League
# semifinal (5-4 after extra time). Their only prior World Cup meeting
# (2006 Round of 16) was won by France, 3-1.
HEAD_TO_HEAD = {
    "team1_win_rate": 0.3,     # France: roughly 3 of the last 10 meetings (Spain won 7)
    "avg_goal_diff": -1.0,     # based on the two most recent meetings, from France's perspective
}

VENUE = {
    "venue_name": "Dallas Stadium (AT&T Stadium), Arlington, Texas",
    "pitch_type": "natural/hybrid grass, retractable-roof stadium",
    "altitude_m": 180,
    "expected_conditions": "Fully enclosed, climate-controlled indoor stadium -- consistent "
                            "conditions regardless of North Texas summer heat outside",
}

# Real past France vs Spain results for backtesting (most notable/recent
# documented meetings found; team1 = France, team2 = Spain)
KNOWN_PAST_RESULTS = [
    # (is_team1_home, team1_goals, team2_goals)
    (False, 4, 5),   # 2025 UEFA Nations League semifinal (AET), Spain won 5-4
    (False, 1, 2),   # Euro 2024 semifinal, Munich (neutral), Spain won 2-1
    (True, 3, 1),    # 2006 World Cup Round of 16, France won 3-1
]