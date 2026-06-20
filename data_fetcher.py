"""
data_fetcher.py
----------------
Handles all calls to the API-Football (via RapidAPI) service.

Sign up for a free key here:  https://www.api-football.com/  (or RapidAPI's "API-FOOTBALL")
Free tier gives 100 requests/day which is plenty for a single matchup.

Set your key as an environment variable before running, e.g.:
    export FOOTBALL_API_KEY="your_key_here"      (Mac/Linux)
    setx FOOTBALL_API_KEY "your_key_here"         (Windows)
"""

import os
import time
import requests

API_KEY = os.environ.get("FOOTBALL_API_KEY", "PUT_YOUR_KEY_HERE")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def _get(endpoint, params=None):
    """Generic GET wrapper with basic rate-limit friendliness."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params or {})
    resp.raise_for_status()
    time.sleep(0.3)  # be nice to the free tier rate limit
    return resp.json().get("response", [])


def get_team_id(team_name):
    """Look up a team's API-Football ID by name."""
    data = _get("teams", {"search": team_name})
    if not data:
        raise ValueError(f"No team found for '{team_name}'")
    # take the most relevant (first) match
    return data[0]["team"]["id"], data[0]["team"]["name"]


def get_fixture_by_teams(team1_id, team2_id, season=None):
    """Find the upcoming fixture between two teams (next scheduled match)."""
    data = _get("fixtures/headtohead", {
        "h2h": f"{team1_id}-{team2_id}",
        "next": 1
    })
    return data[0] if data else None


def get_head_to_head(team1_id, team2_id, last_n=10):
    """Pull historical head-to-head matches between the two teams."""
    data = _get("fixtures/headtohead", {
        "h2h": f"{team1_id}-{team2_id}",
        "last": last_n
    })
    return data


def get_recent_form(team_id, last_n=5):
    """Pull a team's last N matches (any opponent) to compute recent form."""
    data = _get("fixtures", {
        "team": team_id,
        "last": last_n
    })
    return data


def get_league_info(league_id, season):
    """
    Debug helper: check what your API plan actually has access to for this
    league/season (useful for diagnosing free-tier season restrictions).
    """
    return _get("leagues", {"id": league_id, "season": season})


def get_fixtures_by_league(league_id, season, status="FT"):
    """
    Pull all fixtures for a league/season, optionally filtered by status.
    status='FT' = finished matches only (what we want for training data).
    Use status=None to get everything including upcoming fixtures.
    """
    params = {"league": league_id, "season": season}
    if status:
        params["status"] = status
    return _get("fixtures", params)


def get_team_statistics(team_id, league_id, season):
    """
    Season-long aggregate stats for a team in a given league/season:
    win rate, goals scored/conceded averages, clean sheets, etc.
    """
    data = _get("teams/statistics", {
        "team": team_id,
        "league": league_id,
        "season": season
    })
    return data


def get_squad(team_id):
    """Full current squad list for a team."""
    data = _get("players/squads", {"team": team_id})
    if not data:
        return []
    return data[0].get("players", [])


def get_player_statistics(player_id, season):
    """Per-player season stats: rating, goals, assists, minutes played."""
    data = _get("players", {"id": player_id, "season": season})
    return data


def get_venue_info(fixture_id):
    """Venue/pitch info attached to a specific fixture."""
    data = _get("fixtures", {"id": fixture_id})
    if not data:
        return None
    return data[0]["fixture"]["venue"]


def get_venue_history(venue_name, last_n=20):
    """
    Pull historical matches played at a given venue to estimate
    pitch/conditions effects (e.g. high-scoring venue, strong home advantage, etc.)
    NOTE: API-Football doesn't have a direct venue-search endpoint, so in practice
    you'd cross-reference fixtures you've already pulled for teams that play there.
    This is a placeholder you can extend depending on your data source.
    """
    raise NotImplementedError(
        "Venue history requires cross-referencing fixtures by venue name "
        "across competitions. Plug in a venue-specific dataset if you have one, "
        "or aggregate from fixtures you've already fetched."
    )