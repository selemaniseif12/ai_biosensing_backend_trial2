import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ✔ USE THE NEW REALISTIC DATASET
DATASET_PATH = "app/training_v6_stepB_175_realistic.csv"

# ✔ SAVE MODEL TO THE CORRECT BACKEND LOCATION
MODEL_OUTPUT = "app/ml/models/classify/v6/sim_model_v6_175.pkl"

def load_dataset():
    df = pd.read_csv(DATASET_PATH)

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


def train_v6():
    print("Loading realistic Step‑B v6 dataset (175 viruses)...")
    X, y = load_dataset()

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    print("Training RandomForestClassifier (v6, 175 viruses)...")
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=25,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Evaluating v6 175‑virus model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    print(f"Saving v6 model to {MODEL_OUTPUT}...")
    joblib.dump(model, MODEL_OUTPUT)

    print("Training complete. High‑accuracy v6 175‑virus model saved.")


if __name__ == "__main__":
    train_v6()
