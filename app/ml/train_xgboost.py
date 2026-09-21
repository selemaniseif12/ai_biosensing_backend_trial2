import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

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

    X = df[feature_cols]
    y = df["time_to_detection"]
    return X, y

def train_xgboost():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("XGB R²:", r2_score(y_test, y_pred))
    print("XGB MAE:", mean_absolute_error(y_test, y_pred))

    model_path = os.path.join(MODELS_DIR, "xgb_time_to_detection.pkl")
    joblib.dump(model, model_path)
    print("Saved:", model_path)

if __name__ == "__main__":
    train_xgboost()
