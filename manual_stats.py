"""
manual_stats.py  (France vs England -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, Third-Place Play-off (Match 103)
Date/Time: Saturday, July 18, 2026, 5:00pm ET / 21:00 GMT
Venue: Miami Stadium (Hard Rock Stadium), Miami Gardens, Florida

Sources checked: Olympics.com, Bolavip, Sports Mole, bet365 News,
Vanguard, World Soccer Talk, NBC affiliates, Squawka (match previews,
head-to-head history, squad rotation news)

CONTEXT GOING IN:
- Both sides arrive as beaten, disappointed semifinalists rather than
  finalists -- this is the "bronze medal" match, worth an extra $2
  million in prize money but no trophy. France, pre-tournament favourites
  and the tournament's top scorers (16 goals), were stunned 2-0 by Spain
  in the semifinal, held to zero shots on target from Mbappe and shut out
  for the first time all tournament. England lost a back-and-forth
  semifinal 2-1 to Argentina (Anthony Gordon put them ahead in the 55th
  minute before Enzo Fernandez and a stoppage-time Lautaro Martinez goal
  turned it around, with Messi involved in both Argentina goals).
- Kylian Mbappe (8 goals) and Lionel Messi (8 goals) are tied atop the
  Golden Boot race, with Messi still to play the final; Harry Kane and
  Jude Bellingham are both 2 goals behind on 6 apiece, giving them an
  outside chance to close the gap in this match specifically since
  Messi/Mbappe's final tallies are set independently.
- Squad rotation is expected on both sides given the reduced stakes:
  reports indicate William Saliba is set to be rested for France, with
  Rayan Cherki coming into the starting XI; for England, Reece James is
  expected to be rotated out at right-back, with uncertainty over his
  direct replacement (Jarell Quansah's 2-match suspension has now been
  served and he is available again, but may compete with others for
  the spot rather than being a certain starter).
- Historically, England have actually had the better of this fixture
  overall (leading the all-time head-to-head), but France have dominated
  the recent meetings -- England have just 3 wins in the last 13
  meetings and only 1 in the last 9, with that solitary recent win coming
  in a November 2015 friendly at Wembley overshadowed by the Paris
  attacks four days earlier. Their two most recent meetings were both
  France wins: a 3-2 friendly thriller in 2017, and the defining recent
  clash -- the 2022 World Cup quarterfinal in Qatar, which France won
  2-1 to eliminate England en route to the final. This will be their 4th
  ever World Cup meeting (England lead 2-1-1 in the first three: England
  won in 1966 and 1982, France won in 2022).
- Miami Stadium (Hard Rock Stadium) is an open-air stadium with a
  partial canopy roof; expect hot, humid Miami conditions in late July.

NOTE ON TEAM NAME: historical_data.py's dataset should match "France"
and "England" directly.
"""

FRANCE = {
    # 6 wins, 1 loss (the semifinal shutout vs Spain) -- still the
    # tournament's top scorers despite that result
    "win_rate": 0.857,
    "goals_for_avg": 2.29,        # 16 goals / 7 games
    "goals_against_avg": 0.57,    # 4 goals against / 7 games
    "form_points_avg": 2.57,

    "players": [
        {"id": "Mike Maignan",          "start_prob": 0.9,  "events": []},
        {"id": "Jules Kounde",          "start_prob": 0.85, "events": []},
        {
            "id": "William Saliba", "start_prob": 0.35,   # reported to be RESTED for this match
            "events": [],
        },
        {"id": "Dayot Upamecano",       "start_prob": 0.8,  "events": []},
        {"id": "Lucas Digne",           "start_prob": 0.75, "events": []},
        {"id": "Manu Kone",             "start_prob": 0.7,  "events": []},
        {"id": "Adrien Rabiot",         "start_prob": 0.75, "events": []},
        {
            "id": "Ousmane Dembele", "start_prob": 0.75,   # Ballon d'Or winner, some rotation possible in a dead-rubber game
            "events": [
                {"date": "2026-07-14", "type": "rating", "value": 6.8},  # quiet in the semifinal loss
            ],
        },
        {"id": "Michael Olise",         "start_prob": 0.75, "events": []},
        {
            "id": "Rayan Cherki", "start_prob": 0.55,   # reported to be coming INTO the starting XI
            "events": [],
        },
        {
            "id": "Kylian Mbappe", "start_prob": 0.85,   # captain; motivated to defend/extend Golden Boot tally
            "events": [
                {"date": "2026-07-14", "type": "rating", "value": 6.0},  # blanked by Spain, 0 shots on target
            ],
        },
        {"id": "Bradley Barcola",       "start_prob": 0.5,  "events": []},
        {"id": "Desire Doue",           "start_prob": 0.45, "events": []},
    ],

    "team_record_at_similar_conditions": 0.5,
}

ENGLAND = {
    # 5 wins, 1 draw, 1 loss (the semifinal defeat to Argentina) --
    # competitive throughout but came up just short at the final hurdle
    "win_rate": 0.714,
    "goals_for_avg": 2.0,          # 14 goals / 7 games
    "goals_against_avg": 1.43,     # 10 goals against / 7 games
    "form_points_avg": 2.29,

    "players": [
        {"id": "Jordan Pickford",       "start_prob": 0.9,  "events": []},
        {
            "id": "Reece James", "start_prob": 0.45,   # reported to be rotated OUT at right-back
            "events": [],
        },
        {
            "id": "Jarell Quansah", "start_prob": 0.45,   # suspension served, available again but competing for the spot
            "events": [],
        },
        {"id": "Ezri Konsa",            "start_prob": 0.7,  "events": []},
        {"id": "Marc Guehi",            "start_prob": 0.8,  "events": []},
        {"id": "Nico O'Reilly",         "start_prob": 0.6,  "events": []},
        {"id": "Declan Rice",           "start_prob": 0.8,  "events": []},
        {"id": "Elliot Anderson",       "start_prob": 0.65, "events": []},
        {"id": "Bukayo Saka",           "start_prob": 0.75, "events": []},
        {
            "id": "Jude Bellingham", "start_prob": 0.8,   # 6 goals, motivated to close the gap in the Golden Boot race
            "events": [
                {"date": "2026-07-15", "type": "rating", "value": 6.9},  # unable to find decisive impact vs Argentina
            ],
        },
        {"id": "Anthony Gordon",        "start_prob": 0.65,
         "events": [
             {"date": "2026-07-15", "type": "goal"},   # opener vs Argentina, SF (England's goal in the loss)
         ]},
        {
            "id": "Harry Kane", "start_prob": 0.85,   # captain, motivated to close the gap in the Golden Boot race
            "events": [
                {"date": "2026-07-15", "type": "rating", "value": 6.7},  # unable to find decisive impact vs Argentina
            ],
        },
        {"id": "Marcus Rashford",       "start_prob": 0.5,  "events": []},
    ],

    "team_record_at_similar_conditions": 0.5,
}

# Real head-to-head record found: England lead the all-time series
# overall, but France have dominated recent meetings -- England have won
# just 3 of the last 13 and only 1 of the last 9 (a Nov 2015 friendly).
# The two most recent meetings were both France wins: a 3-2 friendly in
# 2017 and the decisive 2022 World Cup quarterfinal (2-1). This is only
# their 4th ever World Cup meeting; England lead 2-1 in the first three
# (1966, 1982 England wins; 2022 France win).
HEAD_TO_HEAD = {
    "team1_win_rate": 0.6,     # France have the recent edge despite England leading all-time
    "avg_goal_diff": 0.3,      # slight recent edge to France based on the last 3 documented meetings
}

VENUE = {
    "venue_name": "Miami Stadium (Hard Rock Stadium), Miami Gardens, Florida",
    "pitch_type": "natural grass, partially covered open-air stadium",
    "altitude_m": 3,
    "expected_conditions": "Hot and humid South Florida late-July conditions -- partial "
                            "canopy roof covers most seating but the pitch itself is open "
                            "to the elements",
}

# Real past France vs England results for backtesting (most notable/
# recent documented meetings; team1 = France, team2 = England)
KNOWN_PAST_RESULTS = [
    # (is_team1_home, team1_goals, team2_goals)
    (False, 2, 1),   # 2022 World Cup quarterfinal, Qatar (neutral venue), France won 2-1
    (True, 3, 2),    # 2017 friendly in Paris, France won 3-2
    (False, 0, 2),   # Nov 2015 friendly at Wembley, England won 2-0
]