import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

DATA_PATH = "app/ml/simulation_training_data.csv"

def train_spectral():
    df = pd.read_csv(DATA_PATH)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    X = df.drop(columns=["virus_id"])
    y = df["virus_id"]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=18,
        random_state=42
    )

    model.fit(X, y)

    save_path = "app/ml/models/classify/spectral/spectral_model.pkl"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)

    print(f"Saved spectral model with {X.shape[1]} features")

if __name__ == "__main__":
    train_spectral()
