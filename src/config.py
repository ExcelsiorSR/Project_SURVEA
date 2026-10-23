# =============================================
#              CENTRAL CONFIGURATION
# =============================================
# Every asset-specific detail (CSV, feature columns, classification label,
# regression target, LSTM support) lives HERE -- so training scripts,
# the predictor, and the live-feed client never hardcode a column name themselves.

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
MODELS_DIR = PROJECT_ROOT / "models"
SCALERS_DIR = MODELS_DIR / "scalers"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
SCALERS_DIR.mkdir(parents=True, exist_ok=True)

# LSTM sliding-window length (how many past readings feed one prediction)
SEQUENCE_LENGTH = 20
RANDOM_STATE = 42

# =============================================
#              ASSET SCHEMAS
# =============================================
# For each asset:
#   csv_file             -- raw file name under data/raw/
#   feature_columns      -- columns fed to BOTH the RF classifier and the LSTM
#   classification_label -- the column the RF classifier predicts
#   class_names          -- ordered so class_names[code] == the display label
#   supports_lstm        -- False means no temporal/RUL signal exists in this dataset (relay)
#   regression_target    -- the column the LSTM predicts
#   higher_is_worse      -- whether higher values of the regression target indicate degradation
#   sort_columns / group_column -- how to order rows into a real time series before windowing

ASSETS = {
    "transformer": {
        "csv_file": "dga_ml_ready.csv",
        "feature_columns": [
            "H2", "CH4", "C2H2", "C2H4", "C2H6", "CO", "CO2", "O2", "H2O",
            "R1_CH4_H2", "R2_C2H2_C2H4", "R3_C2H2_CH4", "R4_C2H4_C2H6", "R5_C2H6_CH4",
            "Duval_CH4_pct", "Duval_C2H4_pct", "Duval_C2H2_pct",
        ],
        "classification_label": "Fault_Code",
        "supports_classification": True,
        "class_names": {
            0: "Normal", 1: "Partial Discharge", 2: "D1 - Low Energy Discharge",
            3: "D2 - High Energy Discharge", 4: "T1 - Thermal Fault (<300C)",
            5: "T2 - Thermal Fault (300-700C)", 6: "T3 - Thermal Fault (>700C)",
            7: "Undetermined",
        },
        "supports_lstm": True,
        # NOTE: No RUL column exists. This dataset is discrete maintenance-log entries per unit
        # (most readings are already past the first fault), not smooth degradation trajectories.
        # The LSTM instead predicts dga_severity_index -- max of the 6 standardized gas readings --
        # which is dense, continuous, and directly comparable to what the Digital Twin tracks.
        "regression_target": "dga_severity_index",
        "higher_is_worse": True,
        "unit_column": "Transformer_ID",
        "time_column": "Timestamp",
        "time_format": "%d/%m/%Y %H:%M",
    },
    "generator": {
        "csv_file": "Generator_dataset.csv",
        "feature_columns": [
            "Bearing_Frequency_Hz", "Bearing_Amplitude_mm_s", "Temperature_C",
            "Temp_Rise_Rate_C_min", "Thermal_Runaway_Indicator",
            "Temp_Above_Normal", "Freq_Deviation",
        ],
        "classification_label": "Fault_Code",
        "supports_classification": True,
        "class_names": {
            0: "Normal", 1: "Moderate Fault", 2: "Severe Fault",
            3: "Thermal Warning", 4: "Thermal Runaway",
        },
        "supports_lstm": True,
        # Health_Index is a genuine continuous column in the dataset (confirmed empirically:
        # rises from ~19 at Fault_Code 0 to ~50 at Fault_Code 4) -- used AS-IS, not fabricated.
        "regression_target": "Health_Index",
        "higher_is_worse": True,
        "unit_column": None,  # single continuous series, no per-unit split
        "time_column": "Timestamp",
        "time_format": "%Y-%m-%d %H:%M:%S",
    },
    "circuit_breaker": {
        "csv_file": "cb_refined_dataset.csv",
        "feature_columns": [
            "TCCS_Peak_Current_A", "TCCS_Duration_ms", "Contact_Travel_Time_ms",
            "Contact_Temperature_C", "Gas_Pressure_bar",
            "Current_Dev", "Travel_Dev", "Temp_Dev", "Pressure_Drop",
        ],
        "classification_label": "Fault_Code",
        "supports_classification": True,
        "class_names": {
            0: "Normal", 1: "Coil Degradation - Early", 2: "Coil Degradation - Severe",
            3: "Friction Wear", 4: "Mechanical Jamming - Mild", 5: "Mechanical Jamming - Severe",
        },
        "supports_lstm": True,
        "regression_target": "Health_Index",
        "higher_is_worse": True,
        "unit_column": None,
        "time_column": "Operation_Number",  # cleaner sequence index than the timestamp string
        "time_format": None,                # numeric, no parsing needed
    },
    "relay": {
        "csv_file": "relay_dataset_F.csv",
        "feature_columns": ["V_rms", "I_rms", "V_peak", "I_peak", "Impedance_Z"],
        "classification_label": "Fault_Class",
        "supports_classification": True,
        # Class names are our own interpretation fitted to per-class V/I/Z averages --
        # no text labels exist in this CSV.
        "class_names": {
            0: "Normal", 1: "Elevated Fault Current",
            2: "Moderate Impedance Fault", 3: "Critical Zone Fault",
        },
        # No timestamp, no unit ID, no operation counter -- flat, independently-shuffled
        # snapshot rows. There is nothing to build a sequence out of. We do NOT fake one.
        # NOTE: this is the live-twin-compatible relay model. The Digital Twin simulates
        # exactly these 5 fields. Do not replace with relay_endurance -- it's a separate
        # asset type on purpose.
        "supports_lstm": False,
        "regression_target": None,
        "higher_is_worse": None,
        "unit_column": None,
        "time_column": None,
        "time_format": None,
    },
    "relay_endurance": {
        # A SEPARATE asset type -- NOT a replacement for "relay" above.
        # Built from a real relay endurance test (100,246 switching operations,
        # waveform-derived features). Physically different quantities from what
        # the Digital Twin simulates, so it cannot feed live twin telemetry.
        # Exists for real-data benchmarking and as the template for extending
        # the twin's own relay model later. See src/data/relay_h5_processor.py.
        "csv_file": "relay_h5_processed.csv",
        "feature_columns": [
            "I_on_peak", "I_on_mean", "I_off_peak", "I_off_mean",
            "U_on_peak", "U_on_mean", "U_off_peak", "U_off_mean",
            "U_on_peak_zscore", "U_off_peak_zscore",
        ],
        "classification_label": "Fault_Code",
        "supports_classification": True,
        # Labels are z-score-based severity buckets of U_on_peak (the clearest wear signal --
        # confirmed empirically: baseline ~24V in first 1000 ops vs >37V in last 1000).
        # Thresholds (z<3 / 3<=z<20 / z>=20) fit to the actual distribution (66.7/19.5/13.8%).
        "class_names": {0: "Normal", 1: "Wear Onset", 2: "Critical Wear"},
        "supports_lstm": True,
        # Real ground-truth RUL -- assumes the last logged operation is actual end-of-life
        # (right-censoring assumption if the log stopped early, unverifiable from the file alone).
        "regression_target": "RUL_operations_remaining",
        "higher_is_worse": False,
        "unit_column": "Relay_Unit_ID",
        "time_column": "Operation_Number",
        "time_format": None,
    },
    "generator_plant_log": {
        # Real hourly plant telemetry -- NOT a replacement for "generator" above.
        # Different feature space entirely (electrical + 4 bearing temps vs
        # Bearing_Amplitude/single Temperature_C) and NO fault labels exist.
        # supports_classification is False on purpose: there is nothing to train against.
        # LSTM-only, same pattern as relay_endurance.
        "csv_file": "steam_alternator_generator_log.csv",
        "feature_columns": [
            "V", "Amp", "W", "Pf", "Hz", "Mech_Load",
            "GenBearing_DE_Temp", "GenBearing_NDE_Temp",
            "AltBearing_DE_Temp", "AltBearing_NDE_Temp",
        ],
        "classification_label": None,
        "class_names": {},
        "supports_classification": False,
        "supports_lstm": True,
        # max_bearing_temp_c = max across all four bearing temps -- same derivation
        # pattern as transformer's dga_severity_index: dense, continuous, physically
        # meaningful, not a fabricated label.
        "regression_target": "max_bearing_temp_c",
        "higher_is_worse": True,
        "unit_column": None,        # single continuous plant log, one machine
        "time_column": "Timestamp", # built from LogDate+LogTime, see loaders.py
        "time_format": "%d-%m-%Y %H:%M:%S",
    },
}

ASSET_TYPES = list(ASSETS.keys())