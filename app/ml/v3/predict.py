from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter()

# ---------------------------------------------------------
# Correct model paths (shared models folder)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # app/ml/v3
ML_ROOT = os.path.dirname(BASE_DIR)                        # app/ml
MODEL_DIR = os.path.join(ML_ROOT, "models")                # app/ml/models

MODEL_PATH = os.path.join(MODEL_DIR, "qcm_virus_classifier_rf.joblib")
ENCODER_PATH = os.path.join(MODEL_DIR, "qcm_virus_label_encoder.joblib")

# Load model + encoder
model = joblib.load(MODEL_PATH)
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
# V3 Prediction Endpoint (enhanced output)
# ---------------------------------------------------------
@router.post("/predict")
def predict_v3(data: QCMInput):
    try:
        features = np.array([
            data.device1, data.device2, data.device3, data.device4, data.device5
        ]).reshape(1, -1)

        class_id = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))
        virus_name = label_encoder.inverse_transform([class_id])[0]

        return {
            "version": "v3",
            "predicted_class_id": int(class_id),
            "predicted_virus": virus_name,
            "confidence": confidence,
            "probabilities": {
                label_encoder.inverse_transform([i])[0]: float(probabilities[i])
                for i in range(len(probabilities))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
