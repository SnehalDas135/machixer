# Machixer -- Football Match Outcome & Scoreline Predictor

Predicts the outcome (win / draw / loss) and most likely final scoreline of
a football match, using a mix of:

- Real historical international match results (tens of thousands of real
  games, not synthetic data)
- Each team's real, current form (win rate, goals, form points) computed
  automatically from that history
- Real head-to-head history between the two specific teams
- Manually researched, real, dated player-level events (goals, assists,
  ratings, injuries) that get decay-weighted by recency into a squad
  strength score
- An XGBoost classifier for the outcome probabilities (primary model)
- An optional comparison table of ~20 additional ML algorithms trained on
  the same data, so you can see how different model families call the
  same match

This is NOT a betting tool and makes no promises of accuracy -- it's a
statistically-grounded estimate built the way real football analytics
models are built (similar in spirit to Dixon-Coles-style approaches),
using whatever real signal is available.

---

## 1. Project files

| File                   | Purpose                                                                 |
|------------------------|--------------------------------------------------------------------------|
| `main.py`               | Entry point. Orchestrates data loading, training, and printing results. |
| `model.py`               | All the machine learning models (XGBoost outcome + score models, and the `ModelZoo` comparison suite). |
| `recency_scoring.py`     | Converts real, dated player events into a single recency-weighted squad strength score. |
| `manual_stats.py`        | Hand-researched, match-specific data: rosters, player events, injuries/suspensions, venue, head-to-head. **You edit this file for every new match.** |
| `historical_data.py`     | Loads and processes the large real historical match dataset (not included in this repo listing, but required -- see Section 4). |
| `demo_data.py`           | Generates fully synthetic data for `--demo` mode (also required, see Section 4). |

---

## 2. How to run it

From the project folder, with all files present:

```bash
# Real mode (recommended) -- uses real historical data + your manual_stats.py
python3 main.py

# Demo mode -- fully synthetic, no internet needed, just to confirm the code runs
python3 main.py --demo
```

Real mode requires an internet connection the first time it downloads the
historical match dataset (a free, public CSV -- no API key or signup
needed).

---

## 3. What happens when you run it (real mode walkthrough)

Running `python3 main.py` does the following, in order:

### Step 1 -- Load real historical data
```
Loading real historical match data for Norway vs England...
Loaded 20573 real matches.
```
Pulls international match results from a free public dataset (matches from
2005 onward by default, configurable via `min_year` in `historical_data.load_results()`).

### Step 2 -- Build leakage-safe training features
```
Building leakage-safe training features from real match history...
Training on 19899 real matches.
```
Converts raw match results into model-ready features (rolling win rates,
goal averages, form points, etc.) computed *only* from data available
before each match -- i.e. no future information leaks into training, which
would make the model artificially "accurate" in a way that wouldn't hold
up on a real unplayed match.

### Step 3 -- Compute each team's real current form
```
Norway real recent form (last 15 matches, through 2026-07-04): win_rate=0.87, ...
England real recent form (last 15 matches, through 2026-07-04): win_rate=0.67, ...
```
Looks at each team's last N real matches (against *any* opponent, not just
each other) to get a live snapshot of current form.

### Step 4 -- Real head-to-head
```
Real head-to-head (last 2 meetings): Norway win rate=0.50, avg goal diff=1.00
```
Pulls the real historical record between these two specific teams from the
dataset. If none exist in the dataset window, it falls back to neutral
defaults (0.5 win rate, 0 goal diff) and tells you so.

### Step 5 -- Player-level squad strength (from `manual_stats.py`)
```
Player-weighted squad strength -> Norway: 7.12, England: 7.45

Norway player scores (computed from real dated events where available):
  Erling Haaland         score=8.94  start_prob=0.95  contribution=8.49  [real data]
  ...
```
This is the one part of the pipeline that isn't automatic -- no free
dataset tracks player-level form, injuries, or lineup probabilities. So you
(or Claude, on request) fill in `manual_stats.py` by hand with real,
sourced information: which players are likely to start (`start_prob`), and
a list of real dated events for each (goals, assists, match ratings,
injuries/suspensions). `recency_scoring.py` then does the actual math --
see Section 5 below for exactly how.

Players tagged `[real data]` had at least one logged event; players tagged
`[DEFAULT (no events logged yet)]` fall back to a neutral baseline score
(6.5/10) because no events were entered for them -- this is intentionally
visible so gaps in the data are obvious rather than hidden.

### Step 6 -- Train the models
```
[OutcomeModel] validation accuracy: 0.583
```
Trains the primary `OutcomeModel` (XGBoost classifier) and
`ScorePredictionModel` (two Poisson XGBoost regressors) on the full
historical dataset, with squad strength and head-to-head blended in as
extra features (see Section 6 for exactly how those are combined).

### Step 7 -- Print the primary prediction
```
=== Norway vs England Prediction ===
Norway win probability:  41.5%
Draw probability:        30.1%
England win probability: 28.4%

Expected goals -> Norway: 1.31  |  England: 1.41
Most likely scoreline: Norway 1 - 1 England  (12.2% chance)

Top 5 most probable scorelines:
  Norway 1-1 England  -- 12.2%
  Norway 0-1 England  -- 9.3%
  ...
```
This is the main output. See Section 7 for exactly what each number means.

### Step 8 -- Backtest (context only, not used by the model)
```
=== Backtest (real past results, for sanity-checking) ===
  Norway 0-1 England -> actual: Away Win
  Norway 0-1 England -> actual: Home Win
  ...
```
Reprints the real past meetings you entered in
`manual_stats.KNOWN_PAST_RESULTS`, purely so you can eyeball them against
the model's prediction. **This list is never fed into the model** -- it's
informational only. See Section 8 for the full explanation of what this
is (and isn't) for.

### Step 9 -- Model comparison table
```
[ModelZoo] Training all comparison models (this can take a little while)...
  trained: Random Forest
  trained: Extra Trees
  ...

=== Model Comparison Table (Norway vs England) ===
Model                   Predicted   England Win %   Draw %   Norway Win %
------------------------------------------------------------------------
Random Forest           Home Win    28.4            30.1     41.5
XGBoost                 Draw        35.2            38.9     25.9
Ridge Classifier        Home Win    --              --       --
...

Consensus across 20 models -> Home Win: 12, Draw: 5, Away Win: 3
```
Trains ~20 different classifier families (see Section 9) on the exact same
feature row, so you can see whether the primary XGBoost call agrees with
other algorithms or is an outlier. This does not change or override the
primary prediction in Step 7 -- it's a separate, additional comparison.

---

## 4. Required files not shown above

Two files are referenced by `main.py` but aren't part of the files
regenerated per-match (they're stable infrastructure, not match-specific):

- **`historical_data.py`** must expose:
  - `load_results(min_year=...)` -- loads/filters the historical match CSV
  - `build_training_dataset(df)` -- returns `(X, y_outcome, y_home_goals, y_away_goals)`
  - `get_current_team_stats(df, team_name)` -- returns a dict with `win_rate`, `goals_for_avg`, `goals_against_avg`, `form_points_avg`, `matches_used`, `last_match_date`
  - `get_head_to_head(df, team1, team2)` -- returns a dict with `matches_found`, `team1_win_rate`, `avg_goal_diff`

- **`demo_data.py`** must expose:
  - `generate_synthetic_dataset()` -- returns `(X, y_outcome, y_home_goals, y_away_goals)` as fully synthetic data, for `--demo` mode

If either is missing, `python3 main.py` (or `--demo`) will fail with an
`ImportError`/`ModuleNotFoundError` -- these are assumed to already exist
in your project folder from earlier setup.

---

## 5. How `recency_scoring.py` works

Real football stats don't exist in the free historical dataset at the
player level, so this module is the "human-researched data + transparent
math" layer.

**The data** (event lists per player) comes from you/research. **The
weighting** (turning those events into one score) is this code.

### Event values (before decay)
| Event type        | Value  |
|--------------------|--------|
| `goal`              | +1.5   |
| `assist`            | +1.0   |
| `start`             | +0.2   |
| `injury_or_out`     | -3.0   |
| `rating`            | uses `(rating_value - 6.5)` directly, i.e. how far above/below a neutral baseline that match performance was |

These are editable constants in `EVENT_VALUES` at the top of the file --
change them and every player's score recomputes automatically next run.

### Recency decay
```
weight(days_ago) = 0.5 ** (days_ago / half_life_days)
```
With the default `half_life_days=180` (~6 months):
- an event today: weight = 1.00
- an event 6 months ago: weight = 0.50
- an event 1 year ago: weight = 0.25
- an event 2 years ago: weight = 0.0625

### Player score formula
```
score = default_baseline (6.5) + weighted_average(event adjustments, using recency weights)
```
This is a baseline **plus** a decayed adjustment, not a raw average of
event values -- a single logged goal shouldn't drag a player's score down
to 1.5 just because 1.5 < 6.5. It nudges the baseline up or down instead.

A player with zero logged events gets the default 6.5 and is flagged as
`real_data=False` so you can see at a glance which players are backed by
real events vs. which are just a placeholder.

### Squad strength formula
```
squad_strength = sum(player_score * player_start_prob) / sum(player_start_prob)
```
A player in great current form who is unlikely to start (`start_prob`
low) contributes little; a player in good form who is expected to start
contributes a lot. This is the number reported as `Player-weighted squad
strength` in Step 5 above.

---

## 6. How player/head-to-head data actually feeds the model

This part matters if you want to understand what the model is really
"looking at":

- `team1_squad_strength`, `team2_squad_strength`, `diff_squad_strength`,
  `h2h_team1_win_rate`, and `h2h_avg_goal_diff` are added as extra training
  columns in `main.py`.
- Because the real historical dataset has no historical squad-strength
  numbers, these training columns are **proxied** from the real
  `diff_win_rate` signal (see the comment block in `run_real()`) just so
  the model learns *some* relationship for them. This means squad strength
  and head-to-head are secondary, supporting signals layered on top of the
  real team-form signal -- not the primary driver of the prediction.
- At prediction time (the single match you care about), the *real*
  `t1_squad_strength`/`t2_squad_strength` (from `recency_scoring.py`) and
  real `h2h_win_rate`/`h2h_goal_diff` (from `historical_data.get_head_to_head`)
  are plugged into that same column, so the live match to be predicted uses
  real values even though the training proxy was synthetic-ish.

---

## 7. What the prediction output actually means

- **Win / Draw / Loss probabilities** -- output of `OutcomeModel`
  (`XGBClassifier`, `multi:softprob` over 3 classes: away win / draw / home
  win). Always sums to 100%.
- **Expected goals (lambda)** -- output of `ScorePredictionModel`, two
  separate `XGBRegressor`s trained with a Poisson objective (`count:poisson`).
  This is the average goal rate for each team, not a whole-number
  prediction -- same general approach used in professional football
  analytics (Dixon-Coles-style modeling), because directly regressing on
  exact scorelines is too noisy to be reliable.
- **Most likely scoreline / Top 5 scorelines** -- built by combining the two
  expected-goals numbers into a full probability grid using independent
  Poisson distributions for each team, then reading off the highest-
  probability cells. Even the single "most likely" scoreline is usually a
  fairly small percentage (probability mass is spread across many
  plausible scorelines) -- that's expected, not a bug.

---

## 8. What the backtest section is (and isn't) for

`KNOWN_PAST_RESULTS` in `manual_stats.py` holds a handful of real past
meetings between the two specific teams (5 by default, going back as far
as reliable results are available).

- **It is:** a plain, human-readable sanity check -- "here's what happened
  the last few times these two played," printed right under the
  prediction so you can eyeball it for context.
- **It is not:** part of the model's training or evaluation. The model
  never sees this list. It has zero mathematical effect on the
  probabilities or expected goals above it.

Real head-to-head signal that *does* feed the model comes from a separate,
automatic source: `historical_data.get_head_to_head()`, pulled from the
full dataset (see Section 6). The `KNOWN_PAST_RESULTS` list is a curated,
manually-verified subset used only for display.

---

## 9. The Model Comparison Table (`ModelZoo`)

`ModelZoo` (in `model.py`) trains ~20 different classifier families on
the exact same feature set as the primary `OutcomeModel`, purely for
comparison -- it never overrides or changes the primary XGBoost
prediction printed earlier.

| Model                  | Family                          |
|-------------------------|----------------------------------|
| Random Forest           | Bagged decision trees            |
| Extra Trees              | Bagged decision trees (extra randomization) |
| Bagging Classifier       | Generic bagging (decision tree base) |
| Stacking Classifier      | Meta-model over RF + XGBoost + KNN |
| XGBoost                  | Gradient-boosted trees (same family as primary model) |
| HistGradientBoosting     | Histogram-based gradient boosting |
| Voting Classifier        | Soft-vote over RF + XGBoost + Gradient Boosting |
| Gradient Boosting        | Classic gradient-boosted trees |
| RBF SVM                  | Support vector machine, RBF kernel |
| AdaBoost                 | Boosted decision stumps |
| KNN                      | K-nearest neighbors (k=15) |
| Polynomial SVM           | Support vector machine, degree-3 polynomial kernel |
| Decision Tree            | Single decision tree |
| Gaussian Naive Bayes     | Probabilistic, Gaussian feature assumption |
| MLP Neural Network       | Feed-forward neural net (64 -> 32 hidden units) |
| Linear SVM                | Support vector machine, linear kernel |
| Ridge Classifier         | Linear model, L2-regularized (no probability output) |
| Logistic Regression      | Linear probabilistic classifier |
| SGD Classifier            | Linear model trained via stochastic gradient descent (log-loss, so it does output probabilities) |
| Bernoulli Naive Bayes    | Probabilistic, binary/boolean feature assumption |

**Notes:**
- All models are trained on the same `StandardScaler`-scaled features as
  the primary model -- no model gets an advantage from different
  preprocessing.
- **Ridge Classifier** has no `predict_proba` method, so its row in the
  table shows `--` for all probability columns and only a hard predicted
  label.
- **Stacking Classifier** is the slowest to train (it runs internal 3-fold
  cross-validation across its base models) -- expect the "training all
  comparison models" step to take noticeably longer than the primary
  model's training step.
- The **consensus line** at the bottom of the table is a simple, unweighted
  majority vote across all models that produced a valid label. It does not
  account for each model's confidence or historical accuracy -- treat it as
  a quick eyeball summary, not a statistically rigorous ensemble.
- Different model families can and do disagree, sometimes sharply
  (e.g. a linear model like Logistic Regression vs. a tree ensemble like
  Random Forest) -- that's expected and part of the point of showing them
  side by side, not a sign something is broken.

---

## 10. Updating `manual_stats.py` for a new match

This is the one file you (or Claude, on request) update by hand before
every new match. It must define:

```python
TEAM1_NAME = {
    "win_rate": ...,           # not actually read by main.py (real form comes from historical_data), kept for reference/manual override
    "goals_for_avg": ...,
    "goals_against_avg": ...,
    "form_points_avg": ...,
    "players": [
        {"id": "Player Name", "start_prob": 0.0-1.0, "events": [
            {"date": "YYYY-MM-DD", "type": "goal" | "assist" | "start" | "injury_or_out"},
            {"date": "YYYY-MM-DD", "type": "rating", "value": 0-10},
            ...
        ]},
        ...
    ],
    "team_record_at_similar_conditions": 0.0-1.0,  # informational, not currently used in the model
}

TEAM2_NAME = { ... same shape ... }

HEAD_TO_HEAD = {
    "team1_win_rate": 0.0-1.0,
    "avg_goal_diff": float,   # (team1 goals - team2 goals) averaged over recent meetings
}

VENUE = {
    "venue_name": str,
    "pitch_type": str,
    "altitude_m": float,
    "expected_conditions": str,
}

KNOWN_PAST_RESULTS = [
    (is_team1_home: bool, team1_goals: int, team2_goals: int),
    ...
]
```

In `main.py`, `TEAM1`/`TEAM2` variable names and `manual_stats.TEAM1_NAME`/
`manual_stats.TEAM2_NAME` attribute names must match the actual team names
for that fixture (e.g. `manual_stats.NORWAY`, `manual_stats.ENGLAND`) --
these get renamed for every new match.

---

## 11. Known limitations / honesty notes

- **No live data feed.** Squad selections, injuries, and player events are
  only as current as the last time `manual_stats.py` was manually updated
  from real sources -- there's no automatic scraping.
- **Squad strength proxy in training** is a simplification (see Section 6)
  because no free historical dataset tracks it -- it's a secondary,
  supporting signal, not the main driver.
- **The backtest section and the Model Comparison consensus are both
  informational, not predictive guarantees.** Neither is a substitute for
  real accuracy testing (e.g. proper train/test evaluation over many past
  matches), which this project does not currently implement.
- **This is a probabilistic estimate, not a certainty** -- treat the
  win/draw/loss percentages and scoreline probabilities as exactly that:
  probabilities, not predictions of a single guaranteed outcome.