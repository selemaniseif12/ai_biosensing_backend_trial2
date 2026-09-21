from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import os
import numpy as np

router = APIRouter()

# Correct model paths (simulation-trained)
MODEL_V2_PATH = "app/ml/models/classify/v2/sim_model.pkl"
MODEL_V6_PATH = "app/ml/models/classify/v6/sim_model.pkl"
MODEL_SPECTRAL_PATH = "app/ml/models/classify/spectral/spectral_model.pkl"

model_v2 = None
model_v6 = None
spectral_model = None


def load_models():
    global model_v2, model_v6

    # Load V2 model
    if model_v2 is None:
        if os.path.exists(MODEL_V2_PATH):
            model_v2 = joblib.load(MODEL_V2_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V2_PATH}")

    # Load V6 model
    if model_v6 is None:
        if os.path.exists(MODEL_V6_PATH):
            model_v6 = joblib.load(MODEL_V6_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V6_PATH}")


def load_spectral_model():
    global spectral_model

    if spectral_model is None:
        if os.path.exists(MODEL_SPECTRAL_PATH):
            spectral_model = joblib.load(MODEL_SPECTRAL_PATH)
        else:
            raise FileNotFoundError(f"Spectral model not found: {MODEL_SPECTRAL_PATH}")


class SimpleClassifyRequest(BaseModel):
    features: list[float]  # MUST match model feature count


# -----------------------------
# V2 CLASSIFIER
# -----------------------------
@router.post("/classify/v2")
def classify_v2(req: SimpleClassifyRequest):
    load_models()
    prediction = model_v2.predict([req.features])[0]

    return {
        "model_version": "v2",
        "input_features": req.features,
        "predicted_virus_id": int(prediction),
        "message": "Classification using V2 completed."
    }


# -----------------------------
# V6 CLASSIFIER
# -----------------------------
@router.post("/classify/v6")
def classify_v6(req: SimpleClassifyRequest):
    load_models()
    prediction = model_v6.predict([req.features])[0]

    return {
        "model_version": "v6",
        "input_features": req.features,
        "predicted_virus_id": int(prediction),
        "message": "Classification using V6 completed."
    }


# -----------------------------
# MULTI-VIRUS CLASSIFIER
# -----------------------------
@router.post("/classify/multi")
def classify_multi(req: SimpleClassifyRequest):
    load_models()

    probs = model_v6.predict_proba([req.features])[0]
    classes = model_v6.classes_

    results = {
        int(classes[i]): float(probs[i])
        for i in range(len(classes))
    }

    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    return {
        "model_version": "v6",
        "input_features": req.features,
        "virus_probabilities": sorted_results,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "Multi-virus classification completed."
    }


# -----------------------------
# SPECTRAL FFT-BASED CLASSIFIER
# -----------------------------
@router.post("/classify/spectral")
def classify_spectral(req: SimpleClassifyRequest):
    load_spectral_model()

    prediction = spectral_model.predict([req.features])[0]
    probs = spectral_model.predict_proba([req.features])[0]
    classes = spectral_model.classes_

    results = {
        int(classes[i]): float(probs[i])
        for i in range(len(classes))
    }

    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    return {
        "model_version": "spectral",
        "input_features": req.features,
        "virus_probabilities": sorted_results,
        "top_prediction": int(prediction),
        "message": "Spectral FFT-based classification completed."
    }
