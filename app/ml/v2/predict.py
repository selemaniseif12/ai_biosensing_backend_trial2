from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter()

# ---------------------------------------------------------
# Correct model paths (models folder is in app/ml/models/)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # app/ml/v2
ML_ROOT = os.path.dirname(BASE_DIR)                            # app/ml
MODEL_DIR = os.path.join(ML_ROOT, "models")                    # app/ml/models

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
# V2 Prediction Endpoint (simple version)
# ---------------------------------------------------------
@router.post("/predict")
def predict_v2(data: QCMInput):
    try:
        features = np.array([
            data.device1, data.device2, data.device3, data.device4, data.device5
        ]).reshape(1, -1)

        class_id = model.predict(features)[0]
        virus_name = label_encoder.inverse_transform([class_id])[0]

        return {
            "version": "v2",
            "predicted_class_id": int(class_id),
            "predicted_virus": virus_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
