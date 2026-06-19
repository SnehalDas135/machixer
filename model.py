"""
model.py
---------
Two models, trained on historical match feature rows:

1. XGBClassifier -> P(Home Win), P(Draw), P(Away Win)
   (this is the upgraded version of the original reel's model)

2. Two XGBRegressors with a Poisson objective -> expected goals for
   each team (lambda_home, lambda_away). These lambdas are then fed
   into a Poisson distribution to simulate the most likely final score.
   This is the standard statistical approach real models use for
   scoreline prediction (similar in spirit to the Dixon-Coles model
   used in professional football analytics) -- you cannot reliably
   predict an exact score by regressing on the score number directly,
   it's too noisy. Predicting expected goals and simulating works much
   better.
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
from scipy.stats import poisson


# ---------------------------------------------------------------------------
# OUTCOME CLASSIFIER (Win / Draw / Loss)
# ---------------------------------------------------------------------------

class OutcomeModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="multi:softprob",
            num_class=3,
            eval_metric="mlogloss",
            random_state=42,
        )
        self.feature_cols = None

    def fit(self, X: "pd.DataFrame", y):
        """
        y should be encoded as: 0 = away win, 1 = draw, 2 = home win
        """
        self.feature_cols = X.columns.tolist()
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        val_acc = self.model.score(X_val, y_val)
        print(f"[OutcomeModel] validation accuracy: {val_acc:.3f}")
        return self

    def predict_proba(self, X_row: "pd.DataFrame"):
        X_row = X_row[self.feature_cols]
        X_scaled = self.scaler.transform(X_row)
        probs = self.model.predict_proba(X_scaled)[0]
        return {
            "away_win": probs[0],
            "draw": probs[1],
            "home_win": probs[2],
        }


# ---------------------------------------------------------------------------
# EXPECTED GOALS REGRESSORS -> SCORELINE SIMULATION
# ---------------------------------------------------------------------------

class ScorePredictionModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.home_model = xgb.XGBRegressor(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            objective="count:poisson", random_state=42,
        )
        self.away_model = xgb.XGBRegressor(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            objective="count:poisson", random_state=42,
        )
        self.feature_cols = None

    def fit(self, X, y_home_goals, y_away_goals):
        self.feature_cols = X.columns.tolist()
        X_scaled = self.scaler.fit_transform(X)
        self.home_model.fit(X_scaled, y_home_goals)
        self.away_model.fit(X_scaled, y_away_goals)
        return self

    def predict_expected_goals(self, X_row):
        X_row = X_row[self.feature_cols]
        X_scaled = self.scaler.transform(X_row)
        lam_home = max(self.home_model.predict(X_scaled)[0], 0.05)
        lam_away = max(self.away_model.predict(X_scaled)[0], 0.05)
        return lam_home, lam_away

    @staticmethod
    def simulate_scoreline(lam_home, lam_away, max_goals=6):
        """
        Build a full probability grid over scorelines 0-0 up to max_goals-max_goals
        using independent Poisson distributions, then return the most likely
        scoreline plus the top 5 most probable scorelines.
        """
        grid = np.zeros((max_goals + 1, max_goals + 1))
        for h in range(max_goals + 1):
            for a in range(max_goals + 1):
                grid[h, a] = poisson.pmf(h, lam_home) * poisson.pmf(a, lam_away)

        # normalize (residual probability mass beyond max_goals is small but let's be clean)
        grid /= grid.sum()

        flat_idx = np.argsort(grid.ravel())[::-1]
        top5 = []
        for idx in flat_idx[:5]:
            h, a = np.unravel_index(idx, grid.shape)
            top5.append({"score": f"{h}-{a}", "probability": float(grid[h, a])})

        most_likely = top5[0]
        return most_likely, top5
