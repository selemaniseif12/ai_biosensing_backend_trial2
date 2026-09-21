import os
import joblib
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

from xgboost import XGBRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICT_MODELS_DIR = os.path.join(BASE_DIR, "predict_models")
os.makedirs(PREDICT_MODELS_DIR, exist_ok=True)

def generate_dummy_data(n_samples=500):
    X = np.random.rand(n_samples, 8)
    y = (X.sum(axis=1) * 10) + np.random.randn(n_samples)
    return X, y

def train_rf(X, y):
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, y)
    path = os.path.join(PREDICT_MODELS_DIR, "rf_model.pkl")
    joblib.dump(rf, path)
    print(f"Saved RF model to {path}")

def train_xgb(X, y):
    xgb = XGBRegressor(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    xgb.fit(X, y)
    path = os.path.join(PREDICT_MODELS_DIR, "xgb_model.pkl")
    joblib.dump(xgb, path)
    print(f"Saved XGB model to {path}")

def train_lstm(X, y):
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, os.path.join(PREDICT_MODELS_DIR, "lstm_scaler.pkl"))

    X_seq = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    model = Sequential()
    model.add(LSTM(32, input_shape=(1, X.shape[1])))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X_seq, y, epochs=10, batch_size=32, verbose=0)

    model_path = os.path.join(PREDICT_MODELS_DIR, "lstm_model.h5")
    model.save(model_path)
    print(f"Saved LSTM model to {model_path}")

def main():
    X, y = generate_dummy_data()
    train_rf(X, y)
    train_xgb(X, y)
    train_lstm(X, y)

if __name__ == "__main__":
    main()
