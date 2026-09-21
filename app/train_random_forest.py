import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "ML_Model_Analyzer_v6_Table.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)

    # Clean device_id to numeric 1–5
    df["device_id"] = df["device_id"].str.replace("Device-", "").str.replace("Device‑", "")
    df["device_id"] = df["device_id"].astype(int)

    # Handle any missing values (simple strategy)
    df = df.dropna(subset=["time_to_detection"])

    feature_cols = [
        "ID",
        "device_id",
        "deposition_rate",
        "temperature",
        "humidity",
        "flow_rate",
        "mass_of_virus_fg",
    ]
    X = df[feature_cols]
    y = df["time_to_detection"]
    return X, y

def train_random_forest():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"RandomForest R²: {r2:.3f}")
    print(f"RandomForest MAE: {mae:.3f}")

    model_path = os.path.join(MODELS_DIR, "rf_time_to_detection.pkl")
    joblib.dump(model, model_path)
    print(f"Saved RandomForest model to: {model_path}")

if __name__ == "__main__":
    train_random_forest()
