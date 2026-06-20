"""
check_access.py
----------------
Quick diagnostic: tells you what your API key/plan actually has access to
for league=1 (World Cup), season=2026. Run this if main.py finds 0 fixtures.

Usage: python3 check_access.py
"""
from data_fetcher import get_league_info

result = get_league_info(1, 2026)

if not result:
    print("No data returned at all for league=1, season=2026.")
    print("This usually means your plan doesn't include this season.")
else:
    for entry in result:
        league = entry.get("league", {})
        seasons = entry.get("seasons", [])
        print(f"League: {league.get('name')} (id={league.get('id')})")
        for s in seasons:
            print(f"  Season {s.get('year')}: current={s.get('current')}")
            coverage = s.get("coverage", {})
            print(f"    Coverage: {coverage}")
