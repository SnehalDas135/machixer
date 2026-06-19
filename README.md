# Morocco vs Scotland — ML Match Predictor

Upgraded version of the "FIFA Cup ML Model in 60s" reel concept, built specifically
to test on today's Morocco vs Scotland match (3:30 kickoff).

## What it predicts
1. **Win / Draw / Loss probabilities** (XGBoost classifier)
2. **Predicted final scoreline** (two Poisson-objective XGBoost regressors ->
   expected goals for each team -> simulated scoreline probabilities)

## What's upgraded vs. the original reel
- Original: team win rate + goals stats only, one XGBoost classifier.
- This version adds:
  - **Player-level weighting**: each player's individual rating is multiplied by
    their probability of actually starting (so an injured/rested star contributes
    less than a confirmed in-form starter).
  - **Head-to-head history** between the two specific teams.
  - **Recent form** (last 5 games), weighted separately from season-long stats.
  - **Differential features** (e.g. `diff_win_rate`) which tend to be more
    predictive than raw stats for either team alone.
  - **Score prediction**, not just win/draw/loss — via expected-goals + Poisson
    simulation, the same statistical family real analytics models use.
  - Venue/pitch feature hook (`features.venue_features`) — needs a venue-history
    dataset to fully populate; left as an extension point since API-Football
    doesn't expose it directly.

## Files
- `data_fetcher.py` — all API-Football calls (team IDs, stats, squads, h2h, etc.)
- `features.py` — turns raw API data into model-ready feature rows
- `training_data.py` — assembles a historical training set from many fixtures
- `demo_data.py` — synthetic dataset so you can test the pipeline with **no API key**
- `model.py` — `OutcomeModel` (classifier) and `ScorePredictionModel` (Poisson regressors)
- `main.py` — ties it together; run modes below

## Setup
```bash
pip install xgboost scikit-learn pandas numpy scipy requests
```

Get a free API key from https://www.api-football.com/ (100 requests/day free tier
is enough for this), then:
```bash
export FOOTBALL_API_KEY="your_key_here"
```

## Run it

**Test the pipeline right now, no API key needed:**
```bash
python main.py --demo
```
This trains on synthetic data and prints a sample Morocco vs Scotland prediction
so you can confirm everything runs before wiring up real data.

**Real prediction (after setting your API key):**
```bash
python main.py
```
Note: `run_live()` in `main.py` has a few `TODO`s marked — mainly around (1)
picking which competition/fixtures to train on historically, and (2) pulling
real per-player ratings + minutes for the start-probability weighting. Those
depend on choices only you can make (which league ID, how far back to train),
so they're left as clearly marked fill-ins rather than guessed at.

## Honest limitations
- I don't have live internet access in the environment I built this in, so I
  could not actually call the API or verify real Morocco vs Scotland numbers —
  the demo mode is the only part I could run/test myself. Run it on your end
  with a real key and check the validation accuracy that prints out; if it's
  barely above the baseline (~45% for 3-class), the feature set needs more
  signal (more historical matches, real player data, etc.) before trusting it
  for money on the line.
- A model trained on ~minutes of setup will NOT beat sportsbook odds reliably.
  Treat this as a learning project / directional signal, not a betting edge.
