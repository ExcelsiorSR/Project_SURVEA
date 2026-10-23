# =============================================
#              MODULE IMPORTS
# =============================================

from dataclasses import dataclass

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score

from src.config import MODELS_DIR, RANDOM_STATE

# =============================================
#              RF FAULT CLASSIFIER
# =============================================
# One reusable Random Forest wrapper for all four asset classes -- the
# training logic itself doesn't differ between a transformer and a relay,
# only which columns and how many classes. Asset-specific behavior lives
# in config.py, not duplicated four times here.


@dataclass
class RFTrainResult:
    asset_type: str
    macro_f1: float
    report: str
    n_train: int
    n_test: int


class AssetFaultClassifier:
    """Wraps a RandomForestClassifier for one asset type, plus the feature
    column order it was trained on (so inference can't silently pass columns
    in the wrong order)."""

    def __init__(self, asset_type: str, feature_columns: list[str], n_estimators: int = 300):
        self.asset_type = asset_type
        self.feature_columns = feature_columns
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=None,
            class_weight="balanced",  # several classes are rare (e.g. transformer D2 has only 14 rows)
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    def fit(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> RFTrainResult:
        X_train, X_test, y_train, y_test = train_test_split(
            X[self.feature_columns], y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
        )
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        return RFTrainResult(
            asset_type=self.asset_type,
            macro_f1=float(f1_score(y_test, y_pred, average="macro")),
            report=classification_report(y_test, y_pred, zero_division=0),
            n_train=len(X_train),
            n_test=len(X_test),
        )

    def predict(self, feature_dict: dict) -> dict:
        """feature_dict must contain every key in self.feature_columns.
        Returns the predicted class code and the model's confidence for it."""
        row = pd.DataFrame([[feature_dict[col] for col in self.feature_columns]], columns=self.feature_columns)
        proba = self.model.predict_proba(row)[0]
        pred_code = int(self.model.classes_[np.argmax(proba)])
        confidence = float(np.max(proba))
        return {"fault_code": pred_code, "confidence": confidence}

    def save(self):
        path = MODELS_DIR / f"{self.asset_type}_rf.pkl"
        joblib.dump({"model": self.model, "feature_columns": self.feature_columns}, path)
        return path

    @classmethod
    def load(cls, asset_type: str) -> "AssetFaultClassifier":
        path = MODELS_DIR / f"{asset_type}_rf.pkl"
        payload = joblib.load(path)
        obj = cls(asset_type, payload["feature_columns"])
        obj.model = payload["model"]
        return obj