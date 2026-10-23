# =============================================
#              MODULE IMPORTS
# =============================================

from src.config import ASSETS, SEQUENCE_LENGTH
from src.data.loaders import get_classification_data, get_regression_sequences
from src.models.rf_classifier import AssetFaultClassifier
from src.models.lstm_rul import AssetRULRegressor

# =============================================
#              TRAINING ORCHESTRATOR
# =============================================
# Trains every model this project needs and saves artifacts to models/.
#
# Run from the project root:
#     python -m src.training.train_all


def train_classifiers():
    print("=" * 70)
    print("TRAINING RANDOM FOREST FAULT CLASSIFIERS (all 4 assets)")
    print("=" * 70)

    for asset_type, schema in ASSETS.items():
        if not schema["supports_classification"]:
            print(f"\n--- {asset_type} --- SKIPPED (no fault labels in source dataset, see config.py)")
            continue

        X, y = get_classification_data(asset_type)
        clf = AssetFaultClassifier(asset_type, schema["feature_columns"])
        result = clf.fit(X, y)
        path = clf.save()

        print(f"\n--- {asset_type} ---")
        print(f"train/test: {result.n_train}/{result.n_test}  macro-F1: {result.macro_f1:.3f}")
        print(result.report)
        print(f"saved -> {path}")


def train_lstm_regressors():
    print("=" * 70)
    print("TRAINING LSTM RUL/DEGRADATION REGRESSORS (transformer, generator, circuit_breaker)")
    print("=" * 70)

    for asset_type, schema in ASSETS.items():
        if not schema["supports_lstm"]:
            print(f"\n--- {asset_type} --- SKIPPED (no temporal signal in source dataset, see config.py)")
            continue

        X_seq, y = get_regression_sequences(asset_type, sequence_length=SEQUENCE_LENGTH)
        n_features = X_seq.shape[2]

        print(f"\n--- {asset_type} --- {X_seq.shape[0]} sequences, target='{schema['regression_target']}'")
        reg = AssetRULRegressor(asset_type, n_features=n_features)
        result = reg.fit(X_seq, y)
        path = reg.save()

        print(f"final train_loss={result.final_train_loss:.4f} val_loss={result.final_val_loss:.4f}")
        print(f"saved -> {path}")


if __name__ == "__main__":
    train_classifiers()
    train_lstm_regressors()
    print("\nAll models trained and saved to models/.")