from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import numpy as np

router = APIRouter()

# Load model
model_v2 = joblib.load("app/ml/models/classify/v2/sim_model_v2_100.pkl")

# Real masses for virus IDs 0–99 (your CSV values)
masses = {
    0: 0.00018, 1: 0.000084, 2: 0.000084, 3: 0.000084, 4: 0.00018,
    5: 0.0002, 6: 0.00007, 7: 0.00009, 8: 0.00003, 9: 0.00003,
    10: 0.00003, 11: 0.00012, 12: 0.00012, 13: 0.00006, 14: 0.000075,
    15: 0.000075, 16: 0.00007, 17: 0.000075, 18: 0.00007, 19: 0.00008,
    20: 0.000075, 21: 0.00006, 22: 0.00009, 23: 0.00011, 24: 0.00015,
    25: 0.00003, 26: 0.00003, 27: 0.00003, 28: 0.0001, 29: 0.00006,
    30: 0.00009, 31: 0.00009, 32: 0.00018, 33: 0.00018, 34: 0.00018,
    35: 0.00018, 36: 0.00018, 37: 0.00015, 38: 0.00015, 39: 0.00015,
    40: 0.00015, 41: 0.00009, 42: 0.00009, 43: 0.00003, 44: 0.00003,
    45: 0.00012, 46: 0.00006, 47: 0.0001, 48: 0.00003, 49: 0.00003,
    50: 0.00003, 51: 0.0001, 52: 0.00009, 53: 0.00008, 54: 0.00005,
    55: 0.00007, 56: 0.000075, 57: 0.000075, 58: 0.00008, 59: 0.00005,
    60: 0.00015, 61: 0.00015, 62: 0.00015, 63: 0.000084, 64: 0.000084,
    65: 0.000084, 66: 0.000084, 67: 0.000084, 68: 0.000084, 69: 0.00003,
    70: 0.00003, 71: 0.00003, 72: 0.00003, 73: 0.00003, 74: 0.00003,
    75: 0.00003, 76: 0.00009, 77: 0.0001, 78: 0.00006, 79: 0.00009,
    80: 0.00015, 81: 0.00003, 82: 0.00008, 83: 0.00003, 84: 0.00003,
    85: 0.00003, 86: 0.00003, 87: 0.00002, 88: 0.00003, 89: 0.00003,
    90: 0.00003, 91: 0.00003, 92: 0.00003, 93: 0.00003, 94: 0.00005,
    95: 0.0001, 96: 0.00003, 97: 0.00003, 98: 0.00012, 99: 0.00012
}

class VirusFeatures(BaseModel):
    features: list[float]
    base_frequency_hz: float | None = None
    measured_frequency_hz: float | None = None

def to_vector(data: VirusFeatures):
    return np.array([data.features])

@router.post("/classify/v2")
def classify_v2(data: VirusFeatures):
    vec = to_vector(data)
    probs = model_v2.predict_proba(vec)[0]
    classes = model_v2.classes_

    virus_probabilities = {
        int(classes[i]): float(probs[i])
        for i in range(len(classes))
    }

    virus_masses_fg = {
        int(classes[i]): masses.get(int(classes[i]), 0.0)
        for i in range(len(classes))
    }

    chart_data = [
        {
            "virus_id": int(classes[i]),
            "probability": float(probs[i]),
            "mass_fg": virus_masses_fg[int(classes[i])]
        }
        for i in range(len(classes))
    ]

    return {
        "model_version": "v2",
        "virus_probabilities": virus_probabilities,
        "virus_masses_fg": virus_masses_fg,
        "chart_data": chart_data,
        "base_frequency_hz": data.base_frequency_hz,
        "measured_frequency_hz": data.measured_frequency_hz
    }
