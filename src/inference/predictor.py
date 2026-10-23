# =============================================
#              MODULE IMPORTS
# =============================================

import numpy as np

from src.config import ASSETS, ASSET_TYPES, SEQUENCE_LENGTH
from src.models.rf_classifier import AssetFaultClassifier
from src.models.lstm_rul import AssetRULRegressor

# =============================================
#              ASSET HEALTH PREDICTOR
# =============================================
# The one object the Streamlit frontend talks to.
# Loads every trained model once (RF classifier for all 4 assets, LSTM
# regressor for the 3 that support it) and exposes:
#
#   predictor.classify(asset_type, feature_dict) -> {fault_code, fault_label, confidence}
#   predictor.forecast(asset_type, sequence)      -> {value, target_name, higher_is_worse} or None
#
# `sequence` for forecast() is a list of SEQUENCE_LENGTH feature_dicts, most
# recent last -- exactly what digital_twin_client produces from a live telemetry
# stream, or what a rolling buffer of real CSV rows looks like in demo mode.


class AssetHealthPredictor:
    def __init__(self):
        self._classifiers = {}
        self._regressors = {}

        for asset_type in ASSET_TYPES:
            if ASSETS[asset_type]["supports_classification"]:
                try:
                    self._classifiers[asset_type] = AssetFaultClassifier.load(asset_type)
                except FileNotFoundError:
                    print(f"[predictor] WARNING: no trained RF classifier found for '{asset_type}'. "
                          f"Run `python -m src.training.train_all` first.")

            if ASSETS[asset_type]["supports_lstm"]:
                try:
                    self._regressors[asset_type] = AssetRULRegressor.load(asset_type)
                except FileNotFoundError:
                    print(f"[predictor] WARNING: no trained LSTM found for '{asset_type}'.")

    def classify(self, asset_type: str, feature_dict: dict) -> dict:
        clf = self._classifiers.get(asset_type)
        if clf is None:
            raise RuntimeError(f"No trained classifier loaded for '{asset_type}'.")

        result = clf.predict(feature_dict)
        class_names = ASSETS[asset_type]["class_names"]
        result["fault_label"] = class_names.get(result["fault_code"], "Unknown")
        return result

    def forecast(self, asset_type: str, sequence: list[dict]):
        """Returns None (not an error) for assets with no LSTM -- e.g. relay,
        which genuinely has no temporal signal to forecast from. Callers
        should treat None as 'not applicable', not 'something broke'."""
        schema = ASSETS[asset_type]
        if not schema["supports_lstm"]:
            return None

        reg = self._regressors.get(asset_type)
        if reg is None:
            raise RuntimeError(f"No trained LSTM loaded for '{asset_type}'.")

        if len(sequence) != SEQUENCE_LENGTH:
            raise ValueError(f"forecast() needs exactly {SEQUENCE_LENGTH} readings, got {len(sequence)}.")

        feature_cols = schema["feature_columns"]
        seq_array = np.array([[reading[col] for col in feature_cols] for reading in sequence], dtype=np.float32)
        predicted_value = reg.predict(seq_array)

        return {
            "value": predicted_value,
            "target_name": schema["regression_target"],
            "higher_is_worse": schema["higher_is_worse"],
        }


# Singleton -- Streamlit re-runs the whole script on every interaction, so
# this gets wrapped in @st.cache_resource at the call site (see frontend pages)
# to avoid reloading every model from disk on every click.
def load_predictor() -> AssetHealthPredictor:
    return AssetHealthPredictor()