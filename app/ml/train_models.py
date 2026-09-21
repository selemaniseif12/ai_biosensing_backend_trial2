import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

DATA_PATH = "app/ml/training_data.csv"

def train_model(version):
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["virus_id"])
    y = df["virus_id"]

    model = RandomForestClassifier(
        n_estimators=200 if version == "v6" else 100,
        max_depth=12 if version == "v6" else 8,
        random_state=42
    )

    model.fit(X, y)

    save_path = f"app/ml/models/classify/{version}/rf_model.pkl"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)

    print(f"Saved {save_path}")

if __name__ == "__main__":
    train_model("v2")
    train_model("v6")
