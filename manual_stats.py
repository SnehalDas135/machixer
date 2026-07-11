"""
manual_stats.py  (Norway vs England -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, Quarter-final (Match 99)
Date/Time: Saturday, July 11, 2026, 5:00pm ET / 10:00pm BST / 21:00 GMT
Venue: Hard Rock Stadium, Miami Gardens, Florida

Sources checked: FIFA.com, Sky Sports, ESPN, Sports Mole, SI.com,
Bolavip, Tips.gg, englandfootball.com (match previews, group stage
recaps, head-to-head history)

CONTEXT GOING IN:
- This is the first-ever meeting between Norway and England at a World
  Cup finals, despite 11 prior meetings in friendlies and qualifiers
  dating back to 1937. England lead the all-time head-to-head 6W-3D-2L,
  scoring 24 goals and conceding just 7, and are unbeaten in the last 4
  meetings since 1993 (two 0-0 draws, then 1-0 wins in 2012 and 2014),
  with Norway failing to score in any of those last 4 games.
- Norway are the surprise package of the tournament, reaching a World
  Cup quarterfinal for the first time in their history. Group stage:
  beat Iraq 4-1, beat Senegal 3-2, then lost 4-1 to France (with Haaland
  rested) but still topped through to the knockouts. They then won their
  first-ever World Cup knockout match, 2-1 over Ivory Coast (an
  86th-minute Haaland winner), and followed it with a stunning 2-1 upset
  of five-time champions Brazil in the Round of 16, Haaland scoring a
  brace. He has scored in each of his last 14 competitive Norway matches
  (27 goals in that run) and has found the net in all 4 of his World Cup
  appearances so far (rested for the France loss).
- England topped Group L: beat Croatia 4-2 (Kane brace, Bellingham),
  drew 0-0 with Ghana, beat Panama 2-0 (Bellingham + Kane, Kane's goal
  made him England's all-time leading World Cup scorer with 11, passing
  Gary Lineker). Round of 32: beat DR Congo 2-1. Round of 16: beat Mexico
  3-2 (a Bellingham brace plus a Kane penalty), surviving a second-half
  red card to right-back Jarell Quansah.
- Jarell Quansah's red card has been elevated to a two-match suspension,
  ruling him OUT of this quarterfinal (and the semifinal if England
  advance). Marc Guehi and Declan Rice both carried minor fitness doubts
  into the game but have since trained fully and are expected to start.
- Norway are reportedly set to bring on Jesper Karlsson/Antonio Nusa-type
  width with Andreas Schjelderup coming into the side, with striker
  Alexander Sorloth dropping among the substitutes in the predicted XI.
- Hard Rock Stadium is an open-air stadium with a partial canopy roof
  covering most seating areas but an open pitch -- expect hot, humid
  Miami conditions in July.

NOTE ON TEAM NAME: historical_data.py's dataset should match "Norway"
and "England" directly.
"""

NORWAY = {
    # 4 wins, 0 draws, 1 loss (to France, with Haaland rested); first
    # ever World Cup quarterfinal in Norway's history
    "win_rate": 0.8,
    "goals_for_avg": 2.4,        # 12 goals / 5 games
    "goals_against_avg": 1.8,    # 9 goals against / 5 games
    "form_points_avg": 2.4,

    "players": [
        {"id": "Orjan Nyland",          "start_prob": 0.9,  "events": []},
        {"id": "Torbjorn Heggem",       "start_prob": 0.8,  "events": []},
        {"id": "Kristoffer Ajer",       "start_prob": 0.85, "events": []},
        {"id": "Leo Ostigard",          "start_prob": 0.8,  "events": []},
        {"id": "Julian Ryerson",        "start_prob": 0.75, "events": []},
        {
            "id": "Martin Odegaard", "start_prob": 0.9,   # captain
            "events": [
                {"date": "2026-06-30", "type": "assist"},   # 3rd straight match with an assist, vs Ivory Coast
            ],
        },
        {"id": "Sander Berge",          "start_prob": 0.8,
         "events": [
             {"date": "2026-06-30", "type": "assist"},   # set up Haaland's winner vs Ivory Coast
         ]},
        {"id": "Patrick Berg",          "start_prob": 0.75, "events": []},
        {
            "id": "Antonio Nusa", "start_prob": 0.8,
            "events": [
                {"date": "2026-06-30", "type": "goal"},   # curling opener vs Ivory Coast
                {"date": "2026-06-30", "type": "rating", "value": 7.9},
            ],
        },
        {
            "id": "Andreas Schjelderup", "start_prob": 0.55,   # tipped to come into the starting XI
            "events": [],
        },
        {
            "id": "Oscar Bobb", "start_prob": 0.55,
            "events": [
                {"date": "2026-06-30", "type": "assist"},   # assist in the Haaland winner build-up
            ],
        },
        {
            "id": "Alexander Sorloth", "start_prob": 0.35,   # reportedly dropping out of the XI
            "events": [],
        },
        {
            "id": "Erling Haaland", "start_prob": 0.95,
            "events": [
                {"date": "2026-06-16", "type": "goal"},   # vs Iraq, group
                {"date": "2026-06-22", "type": "goal"},   # vs Senegal, group
                {"date": "2026-06-30", "type": "goal"},   # 86th-min winner vs Ivory Coast, R32
                {"date": "2026-07-05", "type": "goal"},   # brace game-winner vs Brazil, R16
                {"date": "2026-07-05", "type": "rating", "value": 8.9},
            ],
        },
    ],

    "team_record_at_similar_conditions": 0.5,
}

ENGLAND = {
    # 4 wins, 1 draw, 0 losses; unbeaten in last 6 overall (W5 D1)
    "win_rate": 0.8,
    "goals_for_avg": 2.2,        # 11 goals / 5 games
    "goals_against_avg": 1.2,    # 6 goals against / 5 games
    "form_points_avg": 2.6,

    "players": [
        {"id": "Jordan Pickford",       "start_prob": 0.95, "events": []},
        {
            "id": "Marc Guehi", "start_prob": 0.8,   # minor fitness doubt, has since trained fully
            "events": [],
        },
        {"id": "Ezri Konsa",            "start_prob": 0.7,  "events": []},
        {"id": "John Stones",           "start_prob": 0.65, "events": []},
        {
            "id": "Jarell Quansah", "start_prob": 0.0,   # suspended (red card vs Mexico, 2-match ban)
            "events": [
                {"date": "2026-07-06", "type": "injury_or_out"},
            ],
        },
        {"id": "Nico O'Reilly",         "start_prob": 0.55, "events": []},
        {
            "id": "Declan Rice", "start_prob": 0.85,   # minor fitness doubt, has since trained fully
            "events": [],
        },
        {"id": "Elliot Anderson",       "start_prob": 0.75,
         "events": [
             {"date": "2026-07-06", "type": "rating", "value": 7.6},  # leads England for interceptions/tackles
         ]},
        {
            "id": "Jude Bellingham", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-15", "type": "goal"},   # vs Croatia, group opener
                {"date": "2026-06-27", "type": "goal"},   # vs Panama, group finale
                {"date": "2026-07-05", "type": "goal"},   # brace #1 vs Mexico, R16
                {"date": "2026-07-05", "type": "goal"},   # brace #2 vs Mexico, R16
                {"date": "2026-07-05", "type": "rating", "value": 8.6},
            ],
        },
        {"id": "Bukayo Saka",           "start_prob": 0.85, "events": []},
        {
            "id": "Harry Kane", "start_prob": 0.9,   # captain, England's all-time leading WC scorer
            "events": [
                {"date": "2026-06-15", "type": "goal"},   # penalty vs Croatia
                {"date": "2026-06-15", "type": "goal"},   # 2nd vs Croatia
                {"date": "2026-06-27", "type": "goal"},   # header vs Panama (11th WC goal, record)
                {"date": "2026-07-05", "type": "goal"},   # penalty vs Mexico
                {"date": "2026-07-05", "type": "rating", "value": 8.0},
            ],
        },
        {"id": "Marcus Rashford",       "start_prob": 0.55, "events": []},
    ],

    "team_record_at_similar_conditions": 0.55,
}

# Real head-to-head record found: 11 meetings (friendlies + qualifiers,
# never before at a World Cup). England lead 6W-3D-2L, scoring 24 goals
# and conceding 7. England unbeaten in the last 4 (two 0-0 draws, then
# 1-0 wins in 2012 and 2014), with Norway failing to score in any of
# those last 4 meetings.
HEAD_TO_HEAD = {
    "team1_win_rate": 0.18,    # Norway: 2 wins out of 11
    "avg_goal_diff": -1.55,    # (7 - 24) / 11, from Norway's perspective
}

VENUE = {
    "venue_name": "Hard Rock Stadium, Miami Gardens, Florida",
    "pitch_type": "natural grass, partially covered open-air stadium",
    "altitude_m": 3,
    "expected_conditions": "Hot and humid South Florida July conditions -- partial canopy "
                            "roof covers most seating but the pitch itself is open to the "
                            "elements",
}

# Real past Norway vs England results for backtesting (last 5 real
# meetings found; team1 = Norway, team2 = England)
KNOWN_PAST_RESULTS = [
    # (is_team1_home, team1_goals, team2_goals)
    (True, 0, 1),    # May 2012, friendly in Oslo, England won 1-0 (Ashley Young)
    (False, 0, 1),   # Sept 2014, friendly at Wembley, England won 1-0 (Wayne Rooney penalty)
    (False, 0, 0),   # 1995, friendly, goalless draw
    (True, 0, 0),    # 1994, friendly in Oslo, goalless draw
    (True, 2, 0),    # 1993, World Cup Qualifying in Oslo, Norway won 2-0
]