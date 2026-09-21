import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICT_MODELS_DIR = os.path.join(BASE_DIR, "predict_models")

def main():
    print("DEBUG: cwd =", os.getcwd())
    print("DEBUG: BASE_DIR =", BASE_DIR)
    print("DEBUG: PREDICT_MODELS_DIR =", PREDICT_MODELS_DIR)

    os.makedirs(PREDICT_MODELS_DIR, exist_ok=True)
    print("DEBUG: ensured predict_models/ exists")

    # dummy data
    X = np.random.rand(100, 8)
    y = (X.sum(axis=1) * 10) + np.random.randn(100)

    rf = RandomForestRegressor(n_estimators=10, random_state=42)
    rf.fit(X, y)

    model_path = os.path.join(PREDICT_MODELS_DIR, "rf_model.pkl")
    joblib.dump(rf, model_path)
    print("DEBUG: saved RF model to", model_path)

if __name__ == "__main__":
    main()
