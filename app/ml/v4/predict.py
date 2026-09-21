from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import os
import xgboost as xgb

router = APIRouter()

# ---------------------------------------------------------
# Correct model paths (shared models folder)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # app/ml/v4
ML_ROOT = os.path.dirname(BASE_DIR)                        # app/ml
MODEL_DIR = os.path.join(ML_ROOT, "models")                # app/ml/models

XGB_MODEL_PATH = os.path.join(MODEL_DIR, "qcm_virus_classifier_xgb.json")
ENCODER_PATH = os.path.join(MODEL_DIR, "qcm_virus_label_encoder.joblib")

# Load XGBoost model
xgb_model = xgb.XGBClassifier()
xgb_model.load_model(XGB_MODEL_PATH)

# Load label encoder
label_encoder = joblib.load(ENCODER_PATH)

# ---------------------------------------------------------
# Input schema
# ---------------------------------------------------------
class QCMInput(BaseModel):
    device1: float
    device2: float
    device3: float
    device4: float
    device5: float

# ---------------------------------------------------------
# V4 Prediction Endpoint (XGBoost)
# ---------------------------------------------------------
@router.post("/predict")
def predict_v4(data: QCMInput):
    try:
        features = np.array([
            data.device1, data.device2, data.device3, data.device4, data.device5
        ]).reshape(1, -1)

        # Predict class
        class_id = int(xgb_model.predict(features)[0])

        # Predict probabilities
        probabilities = xgb_model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))

        virus_name = label_encoder.inverse_transform([class_id])[0]

        return {
            "version": "v4",
            "model": "XGBoost",
            "predicted_class_id": class_id,
            "predicted_virus": virus_name,
            "confidence": confidence,
            "probabilities": {
                label_encoder.inverse_transform([i])[0]: float(probabilities[i])
                for i in range(len(probabilities))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
