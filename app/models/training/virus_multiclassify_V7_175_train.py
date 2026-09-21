"""
Virus Multi-classify V7-175 Training Script
Trains on ALL data (because each virus appears only once)
RandomForest fingerprint classifier
"""

import pandas as pd
import numpy as np
import random
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import json

# -------------------------------------------------------------
# Load dataset
# -------------------------------------------------------------
DATA_PATH = "app/models/data/virus_multiclass.csv"
df = pd.read_csv(DATA_PATH)

BASE_F = 1693999.68345656012345

# -------------------------------------------------------------
# Sensor drift simulation
# -------------------------------------------------------------
def tuned_step(threshold: float, window: int):
    scale = 1.0
    if window <= 10:
        scale = 0.05
    elif window <= 20:
        scale = 0.08
    elif window <= 50:
        scale = 0.1
    elif window <= 100:
        scale = 0.15
    else:
        scale = 0.2
    return random.uniform(-threshold, threshold) * scale

def generate_sensor_drift(start_t=0, stop_t=100, threshold=0.1):
    current_second = start_t
    cumulative_drift = 0.0
    drift_values = []
    window = stop_t - start_t

    while current_second <= stop_t:
        step = tuned_step(threshold, window)
        cumulative_drift *= 0.995
        cumulative_drift += step
        measured = BASE_F + cumulative_drift
        drift_values.append(measured - BASE_F)
        current_second += 1

    return np.mean(drift_values)

df["sensor_frequency_offset"] = [
    generate_sensor_drift() for _ in range(len(df))
]

# -------------------------------------------------------------
# Correct feature columns based on your CSV
# -------------------------------------------------------------
feature_cols = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s",
    "sensor_frequency_offset"
]

df["virus_id"] = df["virus_id"].astype(str)

X = df[feature_cols]
y = df["virus_id"]

# -------------------------------------------------------------
# Scale features
# -------------------------------------------------------------
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------------------------------------
# Train on ALL data (NO train/test split)
# -------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=800,
    max_depth=None,
    min_samples_split=2,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42
)

model.fit(X_scaled, y)

# Training accuracy (should be 100%)
accuracy = model.score(X_scaled, y)
print(f"Virus Multi-classify V7-175 Training Accuracy: {accuracy * 100:.2f}%")

# -------------------------------------------------------------
# Save model + metadata
# -------------------------------------------------------------
MODEL_PATH = "app/models/virus_multiclassify_V7_175.pkl"
META_PATH = "app/models/virus_multiclassify_V7_175_meta.json"

joblib.dump(model, MODEL_PATH)

metadata = {
    "version": "Virus Multi-classify V7-175",
    "accuracy": float(accuracy),
    "base_frequency_hz": BASE_F,
    "sensor_feature": "sensor_frequency_offset",
    "parameters": {
        "n_estimators": 800,
        "max_depth": None,
        "min_samples_split": 2,
        "max_features": "sqrt"
    }
}

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=4)

print("Model and metadata saved successfully.")
