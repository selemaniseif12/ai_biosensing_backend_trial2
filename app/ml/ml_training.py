import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "predict_models")
os.makedirs(MODEL_DIR, exist_ok=True)

def train_rf_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    path = os.path.join(MODEL_DIR, "rf_model.pkl")
    joblib.dump(model, path)
    return path

def train_scaler(X):
    scaler = MinMaxScaler()
    scaler.fit(X)
    path = os.path.join(MODEL_DIR, "scaler.pkl")
    joblib.dump(scaler, path)
    return path

def generate_dummy_data(n=500):
    X = np.random.rand(n, 8)
    y = (X.sum(axis=1) * 10) + np.random.randn(n)
    return X, y

def main():
    X, y = generate_dummy_data()
    print("Training RF model...")
    rf_path = train_rf_model(X, y)
    print("Saved:", rf_path)

    print("Training scaler...")
    scaler_path = train_scaler(X)
    print("Saved:", scaler_path)

if __name__ == "__main__":
    main()
