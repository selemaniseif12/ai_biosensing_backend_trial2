import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Path to the Step B v2 dataset
DATASET_PATH = "training_v2_stepB.csv"
MODEL_OUTPUT = "models/model_v2_stepB.pkl"

def load_dataset():
    df = pd.read_csv(DATASET_PATH)

    # Features used for Step B physics-based classification
    feature_cols = [
        "deposition_rate",
        "temperature",
        "humidity",
        "flow_rate",
        "time_to_detection",
        "mass_of_virus_fg",
        "device_id",
        "delta_m_fg",
        "measured_frequency_hz",
        "delta_f_hz",
        "noise_hz",
        "q_factor",
        "harmonic_strength",
        "signal_to_noise_ratio",
        "allan_deviation",
    ]

    X = df[feature_cols].values
    y = df["virus_id"].values

    return X, y


def train_v2():
    print("Loading Step B v2 dataset...")
    X, y = load_dataset()

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    print("Training RandomForestClassifier (v2)...")
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=22,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    print(f"Saving v2 model to {MODEL_OUTPUT}...")
    joblib.dump(model, MODEL_OUTPUT)

    print("Training complete. Model saved.")


if __name__ == "__main__":
    train_v2()
