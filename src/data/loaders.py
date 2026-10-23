# =============================================
#              MODULE IMPORTS
# =============================================

import numpy as np
import pandas as pd

from src.config import ASSETS, DATA_RAW_DIR, SEQUENCE_LENGTH

# =============================================
#              DATA LOADERS
# =============================================
# Loads each SURVEA dataset into a common shape and -- where the dataset
# actually supports it -- builds the sliding-window sequences the LSTM needs.
# Nothing here invents data: every regression target is either a pre-existing
# column (Generator/CB's Health_Index, relay endurance's RUL) or an explicit,
# documented heuristic derived from real sensor readings. Relay gets no
# sequence data at all, because its CSV has none to build one from.


def load_asset_raw(asset_type: str) -> pd.DataFrame:
    """Reads the raw CSV for one asset type, with no transformation."""
    schema = ASSETS[asset_type]
    path = DATA_RAW_DIR / schema["csv_file"]
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def get_classification_data(asset_type: str) -> tuple[pd.DataFrame, pd.Series]:
    """
    Returns (X, y) for training the Random Forest fault classifier.
    y is already integer-coded 0..N matching config.ASSETS[asset_type]["class_names"]
    -- every CSV ships its own Fault_Code/Fault_Class column in that encoding,
    so no LabelEncoder guessing is needed or used.
    """
    schema = ASSETS[asset_type]
    if not schema["supports_classification"]:
        raise ValueError(
            f"'{asset_type}' has no fault labels in its source data -- there is "
            f"nothing to train a classifier against. LSTM/regression only."
        )

    df = load_asset_raw(asset_type)
    df = df.dropna(subset=schema["feature_columns"] + [schema["classification_label"]])

    X = df[schema["feature_columns"]].astype(float)
    y = df[schema["classification_label"]].astype(int)
    return X, y


def _derive_transformer_severity_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    dga_ml_ready.csv has no RUL column, and deriving "days until first fault"
    per Transformer_ID saturates near zero for ~95% of rows -- this dataset
    behaves like discrete maintenance-log entries, not smooth degradation trajectories.

    Instead, computes dga_severity_index = max of the 6 standardized gas readings.
    Dense, continuous, and directly comparable to the Digital Twin's own `dga_score`.
    """
    schema = ASSETS["transformer"]
    df = df.copy()
    df[schema["time_column"]] = pd.to_datetime(
        df[schema["time_column"]], format=schema["time_format"], dayfirst=True, errors="coerce"
    )
    df = df.dropna(subset=[schema["time_column"]])

    gas_cols = ["H2", "CH4", "C2H2", "C2H4", "C2H6", "CO"]
    df["dga_severity_index"] = df[gas_cols].max(axis=1)
    return df


def _derive_plant_log_severity(df: pd.DataFrame) -> pd.DataFrame:
    """
    steam_alternator_generator_log.csv ships separate LogDate/LogTime strings and
    has no fault labels or composite health metric -- just raw hourly sensor readings.

    Builds a combined Timestamp for sequencing and derives max_bearing_temp_c as the
    max across all four bearing temps -- same pattern as dga_severity_index:
    dense, continuous, physically meaningful (whichever bearing runs hottest drives
    failure risk), not a fabricated label.
    """
    df = df.copy()
    df["Timestamp"] = pd.to_datetime(
        df["LogDate"] + " " + df["LogTime"], format="%d-%m-%Y %H:%M:%S", errors="coerce"
    )
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp")

    bearing_cols = ["GenBearing_DE_Temp", "GenBearing_NDE_Temp", "AltBearing_DE_Temp", "AltBearing_NDE_Temp"]
    df["max_bearing_temp_c"] = df[bearing_cols].max(axis=1)
    return df


def get_regression_sequences(asset_type: str, sequence_length: int = SEQUENCE_LENGTH):
    """
    Returns (X_seq, y_seq) for training the LSTM RUL/degradation-trend model:
      X_seq shape = (n_samples, sequence_length, n_features)
      y_seq shape = (n_samples,) -- regression_target value at the step after each window.

    Raises ValueError for assets where supports_lstm is False (relay) --
    callers should check schema["supports_lstm"] first rather than relying on this exception.
    """
    schema = ASSETS[asset_type]
    if not schema["supports_lstm"]:
        raise ValueError(
            f"'{asset_type}' has no temporal/RUL signal in its source dataset "
            f"(no timestamp, no unit ID, no operation counter) -- there is "
            f"nothing to build a sequence out of. Classification only."
        )

    df = load_asset_raw(asset_type)
    df = df.dropna(subset=schema["feature_columns"])

    if asset_type == "transformer":
        df = _derive_transformer_severity_index(df)
        df = df.dropna(subset=[schema["regression_target"]])
    elif asset_type == "generator_plant_log":
        df = _derive_plant_log_severity(df)
        df = df.dropna(subset=[schema["regression_target"]])
    else:
        df = df.sort_values(schema["time_column"]).reset_index(drop=True)
        df = df.dropna(subset=[schema["regression_target"]])

    feature_cols = schema["feature_columns"]
    target_col = schema["regression_target"]
    unit_col = schema.get("unit_column")

    def _windows(group: pd.DataFrame):
        feats = group[feature_cols].to_numpy(dtype=np.float32)
        targets = group[target_col].to_numpy(dtype=np.float32)
        xs, ys = [], []
        for i in range(len(group) - sequence_length):
            xs.append(feats[i:i + sequence_length])
            ys.append(targets[i + sequence_length])
        return xs, ys

    all_x, all_y = [], []
    if unit_col:
        for _, group in df.groupby(unit_col):
            group = group.sort_values(schema["time_column"])
            xs, ys = _windows(group)
            all_x.extend(xs)
            all_y.extend(ys)
    else:
        xs, ys = _windows(df)
        all_x.extend(xs)
        all_y.extend(ys)

    if not all_x:
        raise ValueError(
            f"Not enough rows to build any sequence windows for '{asset_type}' "
            f"at sequence_length={sequence_length}. Reduce sequence_length or "
            f"check that grouping by unit isn't fragmenting the data too much."
        )

    return np.stack(all_x), np.array(all_y, dtype=np.float32)