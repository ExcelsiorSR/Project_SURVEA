# =============================================
#              MODULE IMPORTS
# =============================================

import requests

from src.config import ASSETS

# =============================================
#              DIGITAL TWIN CLIENT
# =============================================
# Bridges the Digital Twin's live telemetry (/asset_health/{grid} endpoint) to
# the EXACT feature schema each trained SURVEA model expects.
#
# This isn't a trivial pass-through: the twin's scenario_engine.py only simulates
# PRIMARY sensor readings. It does not simulate the ENGINEERED columns several
# CSVs also ship (ratio features, Duval percentages, deviation-from-baseline
# features) -- those are derived here, using the real baseline constants found
# in the source CSVs (verified empirically, not guessed).
#
# Where a feature genuinely cannot be reconstructed from what the twin simulates
# (transformer's Duval_*_pct and CO2/O2/H2O -- the Duval triangle needs raw ppm
# values the twin never tracks), this falls back to that class's Normal-condition
# mean from the training data. Documented below and flagged in predictor responses.

DEFAULT_BASE_URL = "http://127.0.0.1:8001"

# Baselines empirically confirmed against the SOURCE CSVs, not the twin's own
# internal baselines (which are different numbers -- e.g. the twin initializes
# Contact_Travel_Time_ms at 32.0ms, but the dataset's Travel_Dev was fit against 41.0ms).
_CB_BASELINES = {"current": 4.3, "travel": 41.0, "temp": 48.0, "pressure": 6.5}
_GEN_BASELINES = {"temp": 40.0, "freq": 50.0}

# Fallback values for transformer features the twin cannot reconstruct --
# Normal-class (Fault_Code==0) means from dga_ml_ready.csv, computed once
# and hardcoded here rather than re-reading the CSV at request time.
_TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS = {
    "CO2": -0.93, "O2": -0.13, "H2O": 0.09,
    "Duval_CH4_pct": 33.3, "Duval_C2H4_pct": 33.3, "Duval_C2H2_pct": 33.3,
}

# Ratio features can explode when a gas reading sits near zero (a legitimate twin
# state -- e.g. C2H6 stays at 0.0 throughout an ARCING fault_mode trajectory).
# Clipping to the training range keeps live inference in-distribution rather than
# feeding the model values orders of magnitude beyond what it was trained on.
_RATIO_CLIP_RANGES = {
    "R1_CH4_H2": (-68.7, 196.6), "R2_C2H2_C2H4": (-509.4, 99.7),
    "R3_C2H2_CH4": (-909.9, 1552.3), "R4_C2H4_C2H6": (-56.4, 28.9),
    "R5_C2H6_CH4": (-452.8, 541.5),
}


def _clipped_ratio(numerator, denominator, ratio_name, eps=1e-6):
    low, high = _RATIO_CLIP_RANGES[ratio_name]
    return max(low, min(high, numerator / (denominator + eps if denominator >= 0 else denominator - eps)))


class DigitalTwinClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, grid: str = "118"):
        self.base_url = base_url.rstrip("/")
        self.grid = grid

    def is_reachable(self) -> bool:
        try:
            requests.get(f"{self.base_url}/", timeout=1.5)
            return True
        except requests.RequestException:
            return False

    def _get_asset_registry(self, grid: str = None) -> dict:
        resp = requests.get(f"{self.base_url}/asset_health/{grid or self.grid}", timeout=5)
        resp.raise_for_status()
        return resp.json()["asset_registry"]

    def get_raw_registry(self, grid: str = None) -> dict:
        """Public entry point for fast fleet-wide scanning (the alert banner) --
        returns the twin's own asset_registry directly WITHOUT running any trained
        classifier. One HTTP call regardless of how many assets exist on the grid."""
        return self._get_asset_registry(grid)

    def get_asset_ids(self, asset_type: str, grid: str = None) -> list:
        """Every real asset_id of this type present on the given grid,
        straight from the twin's own registry keys -- needed because asset counts
        differ between 39-bus and 118-bus (e.g. 9 vs 53 generators)."""
        registry_key = {
            "transformer": "transformers", "generator": "generators",
            "circuit_breaker": "circuit_breakers", "relay": "relays",
        }[asset_type]
        registry = self._get_asset_registry(grid)
        return sorted(int(k) for k in registry[registry_key].keys())

    def get_reading(self, asset_type: str, asset_id: int, grid: str = None) -> dict:
        """Returns one feature_dict, in EXACTLY the shape config.ASSETS
        [asset_type]['feature_columns'] expects, built from the twin's current
        live value for that asset."""
        registry_key = {
            "transformer": "transformers", "generator": "generators",
            "circuit_breaker": "circuit_breakers", "relay": "relays",
        }[asset_type]

        registry = self._get_asset_registry(grid)
        raw = registry[registry_key][str(asset_id)]

        if asset_type == "transformer":
            return self._build_transformer_features(raw)
        elif asset_type == "generator":
            return self._build_generator_features(raw)
        elif asset_type == "circuit_breaker":
            return self._build_cb_features(raw)
        elif asset_type == "relay":
            return self._build_relay_features(raw)
        raise ValueError(f"Unknown asset_type '{asset_type}'")

    @staticmethod
    def _build_transformer_features(raw: dict) -> dict:
        h2, ch4, c2h2, c2h4, c2h6, co = raw["H2"], raw["CH4"], raw["C2H2"], raw["C2H4"], raw["C2H6"], raw["CO"]
        return {
            "H2": h2, "CH4": ch4, "C2H2": c2h2, "C2H4": c2h4, "C2H6": c2h6, "CO": co,
            # not reconstructable from the twin's simulated gas set -- documented fallback:
            "CO2": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["CO2"],
            "O2": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["O2"],
            "H2O": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["H2O"],
            # ratio features -- formula confirmed exact against the source CSV;
            # clipped to training range since near-zero denominator is a legitimate twin state.
            "R1_CH4_H2": _clipped_ratio(ch4, h2, "R1_CH4_H2"),
            "R2_C2H2_C2H4": _clipped_ratio(c2h2, c2h4, "R2_C2H2_C2H4"),
            "R3_C2H2_CH4": _clipped_ratio(c2h2, ch4, "R3_C2H2_CH4"),
            "R4_C2H4_C2H6": _clipped_ratio(c2h4, c2h6, "R4_C2H4_C2H6"),
            "R5_C2H6_CH4": _clipped_ratio(c2h6, ch4, "R5_C2H6_CH4"),
            # true Duval triangle % needs raw ppm the twin never simulates -- documented fallback:
            "Duval_CH4_pct": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["Duval_CH4_pct"],
            "Duval_C2H4_pct": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["Duval_C2H4_pct"],
            "Duval_C2H2_pct": _TRANSFORMER_UNRECONSTRUCTABLE_FALLBACKS["Duval_C2H2_pct"],
        }

    @staticmethod
    def _build_generator_features(raw: dict) -> dict:
        return {
            "Bearing_Frequency_Hz": raw["Bearing_Frequency_Hz"],
            "Bearing_Amplitude_mm_s": raw["Bearing_Amplitude_mm_s"],
            "Temperature_C": raw["Temperature_C"],
            "Temp_Rise_Rate_C_min": raw["Temp_Rise_Rate_C_min"],
            "Thermal_Runaway_Indicator": raw["Thermal_Runaway_Indicator"],
            # derived -- baseline (40C, 60Hz) confirmed exact against the source CSV:
            "Temp_Above_Normal": raw["Temperature_C"] - _GEN_BASELINES["temp"],
            "Freq_Deviation": abs(raw["Bearing_Frequency_Hz"] - _GEN_BASELINES["freq"]),
        }

    @staticmethod
    def _build_cb_features(raw: dict) -> dict:
        return {
            "TCCS_Peak_Current_A": raw["TCCS_Peak_Current_A"],
            "TCCS_Duration_ms": raw["TCCS_Duration_ms"],
            "Contact_Travel_Time_ms": raw["Contact_Travel_Time_ms"],
            "Contact_Temperature_C": raw["Contact_Temperature_C"],
            "Gas_Pressure_bar": raw["Gas_Pressure_bar"],
            # derived -- baselines (4.3A / 41ms / 48C / 6.5bar) confirmed exact against
            # the source CSV's own _Dev columns, NOT the twin's internal init values:
            "Current_Dev": raw["TCCS_Peak_Current_A"] - _CB_BASELINES["current"],
            "Travel_Dev": raw["Contact_Travel_Time_ms"] - _CB_BASELINES["travel"],
            "Temp_Dev": raw["Contact_Temperature_C"] - _CB_BASELINES["temp"],
            "Pressure_Drop": _CB_BASELINES["pressure"] - raw["Gas_Pressure_bar"],
        }

    @staticmethod
    def _build_relay_features(raw: dict) -> dict:
        # full 1:1 match -- the twin simulates exactly the 5 columns relay_dataset_F.csv has.
        return {
            "V_rms": raw["V_rms"], "I_rms": raw["I_rms"], "V_peak": raw["V_peak"],
            "I_peak": raw["I_peak"], "Impedance_Z": raw["Impedance_Z"],
        }