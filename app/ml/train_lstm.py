import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "ML_Model_Analyzer_v6_Table_With_Required_Count.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)

    df["device_id"] = df["device_id"].str.replace("Device-", "").str.replace("Device‑", "")
    df["device_id"] = df["device_id"].astype(int)

    feature_cols = [
        "ID",
        "device_id",
        "deposition_rate",
        "temperature",
        "humidity",
        "flow_rate",
        "mass_of_virus_fg",
        "required_virus_count"
    ]

    X = df[feature_cols].values.astype("float32")
    y = df["time_to_detection"].values.astype("float32")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_seq = np.expand_dims(X_scaled, axis=1)
    return X_seq, y, scaler

def build_lstm(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        LSTM(32),
        Dense(16, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model

def train_lstm():
    X, y, scaler = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = build_lstm((X_train.shape[1], X_train.shape[2]))

    model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=80,
        batch_size=8,
        verbose=1
    )

    model.save(os.path.join(MODELS_DIR, "lstm_time_to_detection.h5"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "lstm_scaler.pkl"))

if __name__ == "__main__":
    train_lstm()
