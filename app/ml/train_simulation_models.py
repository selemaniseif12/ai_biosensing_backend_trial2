import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

DATA_PATH = "app/ml/simulation_training_data.csv"

def train_model(version):
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Remove accidental extra columns (Unnamed: 0, index columns, etc.)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Ensure correct columns exist
    required_cols = [
        "base_frequency_hz",
        "noise_hz",
        "delta_f_hz",
        "measured_frequency_hz",
        "virus_id"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Split features and label
    X = df.drop(columns=["virus_id"])
    y = df["virus_id"]

    # Choose model parameters
    model = RandomForestClassifier(
        n_estimators=200 if version == "v6" else 100,
        max_depth=12 if version == "v6" else 8,
        random_state=42
    )

    # Train model
    model.fit(X, y)

    # Save model
    save_path = f"app/ml/models/classify/{version}/sim_model.pkl"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)

    print(f"Saved {save_path} (trained on {X.shape[1]} features)")

if __name__ == "__main__":
    train_model("v2")
    train_model("v6")
