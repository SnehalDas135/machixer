"""
manual_stats.py  (Spain vs Argentina -- FILLED WITH REAL DATA)
------------------------------------------------------------------
Match: FIFA World Cup 2026, FINAL
Date/Time: Sunday, July 19, 2026, 3:00pm ET / 8:00pm BST
Venue: New York/New Jersey Stadium (MetLife Stadium), East Rutherford, NJ

Sources checked: ESPN, ABC News, NBC News, beIN Sports, Yahoo Sports,
FIFA.com, Flashscore, FOX Sports, PBS News (semifinal match reports,
head-to-head history, tournament recaps)

CONTEXT GOING IN:
- The two last teams standing at the first-ever 48-team World Cup, and
  the first-ever World Cup Final meeting between these two countries.
  Argentina are the reigning champions (Qatar 2022) chasing back-to-back
  titles and a 4th star; Spain are chasing their 2nd title (their only
  prior triumph came in South Africa 2010).
- Argentina reached the final with a perfect 7-0-0 record, but have
  needed extra time or late comebacks in 4 of their last 5 games: an
  extra-time win over Cape Verde (R32), a stunning comeback from 2-0 down
  to beat Egypt 3-2 (R16), an extra-time win over 10-man Switzerland 3-1
  (QF), and a 2-1 semifinal win over England where Anthony Gordon put
  England ahead before Enzo Fernandez equalized and Lautaro Martinez
  scored a stoppage-time winner. Messi has 8 goals this tournament
  (level with Mbappe for the Golden Boot lead before the semis, though
  Mbappe and France have now been eliminated) but has gone two straight
  games without scoring himself (the Switzerland QF and England SF),
  while still being heavily involved creatively.
- Spain reached the final with a 6-1-0 record and an extraordinary
  defensive campaign: they have conceded just ONE goal in the entire
  tournament (a Charles De Ketelaere header for Belgium in the
  quarterfinal, which snapped goalkeeper Unai Simon's World Cup-record
  650-minute shutout streak). Full record: Cape Verde 0-0 (group), Saudi
  Arabia 4-0, Uruguay 1-0, Austria 3-0 (R32), Portugal 1-0 (R16), Belgium
  2-1 (QF, Fabian Ruiz and Mikel Merino scoring), and a commanding 2-0
  semifinal win over France (Mikel Oyarzabal penalty, Pedro Porro second
  goal) that ended France's run and stopped Mbappe from getting a single
  shot on target. This is the third summer in a row Spain have beaten
  France in a major semifinal (Euro 2024, 2025 Nations League, now this).
- Mikel Oyarzabal now has 5 tournament goals; Lamine Yamal (who turned 19
  the day before the France semifinal) has been directly involved in
  several of Spain's biggest moments, including winning the penalty
  against France. Mikel Merino has scored a knockout-stage goal off the
  bench in 2 of Spain's last 3 games.
- Historically, Spain and Argentina have met 14 times, with each side
  winning 6 and 2 draws -- a genuinely even head-to-head. They have only
  met once before at a World Cup, the 1966 group stage, which Argentina
  won 2-1. Their most recent meeting was a 2018 friendly, which Spain won
  emphatically 6-1 (an Isco hat-trick).
- No new injury/suspension news reported for either squad heading into
  the final beyond what already applied in the semifinals.
- MetLife Stadium is a large, open-air outdoor stadium (no roof).

NOTE ON TEAM NAME: historical_data.py's dataset should match "Spain"
and "Argentina" directly.
"""

SPAIN = {
    # 6 wins, 1 draw, 0 losses; conceded just ONE goal in the entire
    # tournament (a genuinely historic defensive campaign)
    "win_rate": 0.857,
    "goals_for_avg": 1.86,        # 13 goals / 7 games
    "goals_against_avg": 0.14,    # 1 goal against / 7 games
    "form_points_avg": 2.71,

    "players": [
        {
            "id": "Unai Simon", "start_prob": 0.95,
            "events": [
                {"date": "2026-06-15", "type": "rating", "value": 7.0},
                {"date": "2026-07-10", "type": "injury_or_out"},   # symbolic negative event: streak snapped, conceded first goal of the tournament
            ],
        },
        {"id": "Pedro Porro",           "start_prob": 0.85,
         "events": [
             {"date": "2026-07-14", "type": "goal"},   # 2nd goal vs France, SF, give-and-go with Olmo
             {"date": "2026-07-14", "type": "rating", "value": 7.9},
         ]},
        {
            "id": "Pau Cubarsi", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-10", "type": "rating", "value": 8.4},  # Man of the Match vs Belgium, QF
            ],
        },
        {"id": "Aymeric Laporte",       "start_prob": 0.85, "events": []},
        {"id": "Marc Cucurella",        "start_prob": 0.85, "events": []},
        {"id": "Rodri",                 "start_prob": 0.9,  "events": []},   # captain, midfield anchor
        {
            "id": "Fabian Ruiz", "start_prob": 0.6,   # surprise starter vs Belgium, delivered
            "events": [
                {"date": "2026-07-10", "type": "goal"},   # opener vs Belgium, QF
            ],
        },
        {"id": "Dani Olmo",             "start_prob": 0.85,
         "events": [
             {"date": "2026-07-14", "type": "assist"},   # assist for Porro vs France, SF
         ]},
        {
            "id": "Lamine Yamal", "start_prob": 0.9,
            "events": [
                {"date": "2026-06-21", "type": "goal"},
                {"date": "2026-07-14", "type": "assist"},   # won the penalty vs France, SF (turned 19 the day before)
                {"date": "2026-07-14", "type": "rating", "value": 8.3},
            ],
        },
        {"id": "Alex Baena",            "start_prob": 0.55, "events": []},
        {
            "id": "Mikel Oyarzabal", "start_prob": 0.85,
            "events": [
                {"date": "2026-06-15", "type": "goal"},
                {"date": "2026-06-21", "type": "goal"},
                {"date": "2026-06-26", "type": "goal"},
                {"date": "2026-07-02", "type": "goal"},
                {"date": "2026-07-14", "type": "goal"},   # penalty vs France, SF -- 5th tournament goal
                {"date": "2026-07-14", "type": "rating", "value": 7.8},
            ],
        },
        {
            "id": "Mikel Merino", "start_prob": 0.4,   # impact sub, scored in 2 of last 3 games
            "events": [
                {"date": "2026-07-06", "type": "goal"},   # winner vs Portugal, R16
                {"date": "2026-07-10", "type": "goal"},   # winner vs Belgium, QF
            ],
        },
        {"id": "Pedri",                 "start_prob": 0.5,  "events": []},
    ],

    "team_record_at_similar_conditions": 0.6,
}

ARGENTINA = {
    # Perfect 7-0-0 record, the only unbeaten AND undrawn team in the
    # tournament, but have needed extra time or late drama in 4 of their
    # last 5 games -- a champion team that wins ugly as often as pretty
    "win_rate": 1.0,
    "goals_for_avg": 2.71,       # 19 goals / 7 games
    "goals_against_avg": 1.0,    # 7 goals against / 7 games
    "form_points_avg": 3.0,

    "players": [
        {"id": "Emiliano Martinez",     "start_prob": 0.95, "events": []},
        {"id": "Nahuel Molina",         "start_prob": 0.7,  "events": []},
        {
            "id": "Cristian Romero", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-07", "type": "goal"},   # header vs Egypt, R16 comeback
            ],
        },
        {"id": "Nicolas Otamendi",      "start_prob": 0.75, "events": []},
        {"id": "Nicolas Tagliafico",    "start_prob": 0.6,  "events": []},
        {
            "id": "Enzo Fernandez", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-07", "type": "goal"},   # dramatic stoppage-time winner vs Egypt, R16
                {"date": "2026-07-15", "type": "goal"},   # equalizer vs England, SF
                {"date": "2026-07-15", "type": "rating", "value": 8.2},
            ],
        },
        {"id": "Rodrigo De Paul",       "start_prob": 0.85, "events": []},
        {
            "id": "Alexis Mac Allister", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-11", "type": "goal"},   # opener vs Switzerland, QF (assisted by Messi)
            ],
        },
        {
            "id": "Julian Alvarez", "start_prob": 0.85,
            "events": [
                {"date": "2026-07-11", "type": "goal"},   # extra-time goal vs Switzerland, QF
            ],
        },
        {
            "id": "Lautaro Martinez", "start_prob": 0.8,
            "events": [
                {"date": "2026-07-11", "type": "goal"},   # extra-time goal vs Switzerland, QF
                {"date": "2026-07-15", "type": "goal"},   # stoppage-time winner vs England, SF
                {"date": "2026-07-15", "type": "rating", "value": 8.6},
            ],
        },
        {
            "id": "Lionel Messi", "start_prob": 0.9,   # captain
            "events": [
                {"date": "2026-06-16", "type": "goal"},
                {"date": "2026-06-16", "type": "goal"},
                {"date": "2026-06-16", "type": "goal"},   # hat-trick vs Algeria, group
                {"date": "2026-06-22", "type": "goal"},
                {"date": "2026-06-22", "type": "goal"},   # brace vs Austria, group
                {"date": "2026-06-27", "type": "goal"},   # vs Jordan, group
                {"date": "2026-07-03", "type": "goal"},   # vs Cape Verde, R32
                {"date": "2026-07-07", "type": "goal"},   # 21st WC finals goal (record), vs Egypt R16
                {"date": "2026-07-11", "type": "assist"},  # assisted Mac Allister vs Switzerland, QF
                {"date": "2026-07-15", "type": "rating", "value": 7.5},  # 2nd straight game without a goal, still involved
            ],
        },
        {"id": "Giovani Lo Celso",      "start_prob": 0.5,  "events": []},
        {
            "id": "Leonardo Balerdi", "start_prob": 0.0,   # pre-tournament injury, still out
            "events": [{"date": "2026-06-01", "type": "injury_or_out"}],
        },
    ],

    "team_record_at_similar_conditions": 0.6,
}

# Real head-to-head record found: 14 all-time meetings, each side winning
# 6 with 2 draws -- a genuinely even historical rivalry. Only one prior
# World Cup meeting (1966 group stage, Argentina won 2-1); most recent
# meeting was a 2018 friendly which Spain won 6-1 (Isco hat-trick).
HEAD_TO_HEAD = {
    "team1_win_rate": 0.43,    # Spain: 6 wins out of 14
    "avg_goal_diff": 2.0,      # based on the two specific scorelines found (skewed by the 2018 rout); overall series is much closer (6-6-2)
}

VENUE = {
    "venue_name": "New York/New Jersey Stadium (MetLife Stadium), East Rutherford, NJ",
    "pitch_type": "natural grass, open-air stadium",
    "altitude_m": 3,
    "expected_conditions": "Outdoor, no roof -- typical late-July New Jersey summer "
                            "conditions, warm and potentially humid",
}

# Real past Spain vs Argentina results for backtesting (the only two
# well-documented meetings found; team1 = Spain, team2 = Argentina)
KNOWN_PAST_RESULTS = [
    # (is_team1_home, team1_goals, team2_goals)
    (True, 6, 1),    # 2018 friendly (Seville), Spain won 6-1 (Isco hat-trick)
    (False, 1, 2),   # 1966 World Cup group stage (England, neutral-ish), Argentina won 2-1
]