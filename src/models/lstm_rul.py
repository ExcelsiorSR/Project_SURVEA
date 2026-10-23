# =============================================
#              MODULE IMPORTS
# =============================================

from dataclasses import dataclass

import joblib
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from src.config import MODELS_DIR, SCALERS_DIR, RANDOM_STATE

torch.manual_seed(RANDOM_STATE)

# =============================================
#              LSTM RUL REGRESSOR
# =============================================
# One reusable LSTM regressor for the three asset classes that actually have
# a temporal/degradation signal (transformer, generator, circuit_breaker --
# NOT relay, see config.py). Predicts regression_target's next value from a
# window of past sensor readings.


@dataclass
class LSTMTrainResult:
    asset_type: str
    final_train_loss: float
    final_val_loss: float
    epochs_run: int


class _LSTMNet(nn.Module):
    def __init__(self, n_features: int, hidden_size: int = 64, num_layers: int = 2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=n_features, hidden_size=hidden_size,
            num_layers=num_layers, batch_first=True, dropout=0.2
        )
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, (h_n, _) = self.lstm(x)
        return self.head(h_n[-1]).squeeze(-1)


class AssetRULRegressor:
    """Wraps the LSTM + the feature-scaler it was trained with.
    Both features AND target are standardized -- sensor units span orders of
    magnitude (e.g. mm/s vibration vs standardized DGA gas readings), so raw
    values would blow up the loss for whichever feature has the largest scale."""

    def __init__(self, asset_type: str, n_features: int, hidden_size: int = 64):
        self.asset_type = asset_type
        self.n_features = n_features
        self.model = _LSTMNet(n_features, hidden_size=hidden_size)
        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

    def fit(self, X_seq: np.ndarray, y: np.ndarray, epochs: int = 15, batch_size: int = 256,
            lr: float = 1e-3, test_size: float = 0.2, max_train_samples: int = 200_000) -> LSTMTrainResult:
        # Subsample the TRAINING split only for large datasets (generator: ~500k rows) --
        # the held-out validation split is never subsampled so the reported val loss stays honest.
        X_train, X_val, y_train, y_val = train_test_split(
            X_seq, y, test_size=test_size, random_state=RANDOM_STATE
        )
        if len(X_train) > max_train_samples:
            rng = np.random.RandomState(RANDOM_STATE)
            idx = rng.choice(len(X_train), max_train_samples, replace=False)
            X_train, y_train = X_train[idx], y_train[idx]

        n_samples, seq_len, n_feat = X_train.shape
        self.x_scaler.fit(X_train.reshape(-1, n_feat))
        self.y_scaler.fit(y_train.reshape(-1, 1))

        def _prep(X, y):
            Xs = self.x_scaler.transform(X.reshape(-1, n_feat)).reshape(X.shape)
            ys = self.y_scaler.transform(y.reshape(-1, 1)).ravel()
            return torch.tensor(Xs, dtype=torch.float32), torch.tensor(ys, dtype=torch.float32)

        X_train_t, y_train_t = _prep(X_train, y_train)
        X_val_t, y_val_t = _prep(X_val, y_val)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        final_train_loss, final_val_loss = None, None
        for epoch in range(epochs):
            self.model.train()
            perm = torch.randperm(len(X_train_t))
            epoch_loss = 0.0
            for i in range(0, len(perm), batch_size):
                batch_idx = perm[i:i + batch_size]
                xb, yb = X_train_t[batch_idx], y_train_t[batch_idx]

                optimizer.zero_grad()
                pred = self.model(xb)
                loss = loss_fn(pred, yb)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * len(batch_idx)

            final_train_loss = epoch_loss / len(X_train_t)

            self.model.eval()
            with torch.no_grad():
                val_pred = self.model(X_val_t)
                final_val_loss = loss_fn(val_pred, y_val_t).item()

            print(f"  [{self.asset_type} LSTM] epoch {epoch + 1}/{epochs} "
                  f"train_loss={final_train_loss:.4f} val_loss={final_val_loss:.4f}")

        return LSTMTrainResult(
            asset_type=self.asset_type,
            final_train_loss=final_train_loss,
            final_val_loss=final_val_loss,
            epochs_run=epochs,
        )

    def predict(self, sequence: np.ndarray) -> float:
        """sequence shape = (sequence_length, n_features), most-recent reading last.
        Returns the predicted regression_target value in its ORIGINAL (unscaled) units."""
        self.model.eval()
        x = self.x_scaler.transform(sequence).reshape(1, *sequence.shape)
        with torch.no_grad():
            pred_scaled = self.model(torch.tensor(x, dtype=torch.float32)).item()
        return float(self.y_scaler.inverse_transform([[pred_scaled]])[0, 0])

    def save(self):
        model_path = MODELS_DIR / f"{self.asset_type}_lstm.pt"
        scaler_path = SCALERS_DIR / f"{self.asset_type}_lstm_scalers.pkl"
        torch.save(
            {"state_dict": self.model.state_dict(), "n_features": self.n_features},
            model_path,
        )
        joblib.dump({"x_scaler": self.x_scaler, "y_scaler": self.y_scaler}, scaler_path)
        return model_path

    @classmethod
    def load(cls, asset_type: str) -> "AssetRULRegressor":
        model_path = MODELS_DIR / f"{asset_type}_lstm.pt"
        scaler_path = SCALERS_DIR / f"{asset_type}_lstm_scalers.pkl"

        checkpoint = torch.load(model_path, weights_only=False)
        obj = cls(asset_type, n_features=checkpoint["n_features"])
        obj.model.load_state_dict(checkpoint["state_dict"])

        scalers = joblib.load(scaler_path)
        obj.x_scaler = scalers["x_scaler"]
        obj.y_scaler = scalers["y_scaler"]
        return obj