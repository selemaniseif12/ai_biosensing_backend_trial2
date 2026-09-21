from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import numpy as np

router = APIRouter()

# Load trained 8‑feature, 100‑virus models
model_v2 = joblib.load("sim_model_v2_100.pkl")
model_v6 = joblib.load("sim_model_v6_100.pkl")

# ---------------------------------------------------------
# REAL VIRUS MASS TABLE (fg)
# ---------------------------------------------------------
virus_mass_fg = {
    1: 0.00018, 2: 0.000084, 3: 0.000084, 4: 0.000084, 5: 0.00018,
    6: 0.0002, 7: 0.00007, 8: 0.00009, 9: 0.00003, 10: 0.00003,
    11: 0.00003, 12: 0.00012, 13: 0.00012, 14: 0.00006, 15: 0.000075,
    16: 0.000075, 17: 0.00007, 18: 0.000075, 19: 0.00007, 20: 0.00008,
    21: 0.000075, 22: 0.00006, 23: 0.00009, 24: 0.00011, 25: 0.00015,
    26: 0.00003, 27: 0.00003, 28: 0.00003, 29: 0.0001, 30: 0.00006,
    31: 0.00009, 32: 0.00009, 33: 0.00018, 34: 0.00018, 35: 0.00018,
    36: 0.00018, 37: 0.00018, 38: 0.00015, 39: 0.00015, 40: 0.00015,
    41: 0.00015, 42: 0.00009, 43: 0.00009, 44: 0.00003, 45: 0.00003,
    46: 0.00012, 47: 0.00006, 48: 0.0001, 49: 0.00003, 50: 0.00003,
    51: 0.00003, 52: 0.0001, 53: 0.00009, 54: 0.00008, 55: 0.00005,
    56: 0.00007, 57: 0.000075, 58: 0.000075, 59: 0.00008, 60: 0.00005,
    61: 0.00015, 62: 0.00015, 63: 0.00015, 64: 0.000084, 65: 0.000084,
    66: 0.000084, 67: 0.000084, 68: 0.000084, 69: 0.000084, 70: 0.00003,
    71: 0.00003, 72: 0.00003, 73: 0.00003, 74: 0.00003, 75: 0.00003,
    76: 0.00003, 77: 0.00009, 78: 0.0001, 79: 0.00006, 80: 0.00009,
    81: 0.00015, 82: 0.00003, 83: 0.00008, 84: 0.00003, 85: 0.00003,
    86: 0.00003, 87: 0.00002, 88: 0.00003, 89: 0.00003, 90: 0.00003,
    91: 0.00003, 92: 0.00003, 93: 0.00003, 94: 0.00005, 95: 0.0001,
    96: 0.00003, 97: 0.00003, 98: 0.00012, 99: 0.00012, 100: 0.00006
}

# ---------------------------------------------------------
# REAL DEVICE SENSITIVITY TABLE (fg)
# ---------------------------------------------------------
device_sensitivity_fg = {
    1: 1200,
    2: 1.23,
    3: 900,
    4: 700,
    5: 500
}

# ---------------------------------------------------------
# VIRUS NAMES (partial, extend as needed)
# ---------------------------------------------------------
virus_names = {
    1: "COVID‑19 (SARS‑CoV‑2)",
    2: "Influenza A (H1N1)",
    3: "Influenza A (H3N2)",
    4: "Influenza B",
    5: "SARS‑CoV‑1",
    6: "MERS‑CoV",
    7: "RSV‑A",
    8: "RSV‑B",
    9: "Rhinovirus A",
    10: "Rhinovirus B",
    # ... continue up to 100 if you want names everywhere
}

class VirusFeatures(BaseModel):
    base_frequency_hz: float
    mass_sensitivity: float
    delta_m: float
    delta_m_over_m: float
    delta_f_hz: float
    noise_hz: float
    measured_frequency_hz: float
    quality_factor: float
    device_id: int

def to_vector(data: VirusFeatures):
    return np.array([
        data.base_frequency_hz,
        data.mass_sensitivity,
        data.delta_m,
        data.delta_m_over_m,
        data.delta_f_hz,
        data.noise_hz,
        data.measured_frequency_hz,
        data.quality_factor
    ]).reshape(1, -1)

# ---------------------------------------------------------
# MULTI‑CLASSIFY (physics + IDs + aligned masses)
# ---------------------------------------------------------
@router.post("/classify/multi")
def classify_multi(data: VirusFeatures):
    vec = to_vector(data)

    # Use v6 as your main multi‑virus classifier
    pred_v6 = int(model_v6.predict(vec)[0])
    probs_v6 = model_v6.predict_proba(vec)[0].tolist()

    # Physics: use virus mass + device sensitivity
    m = virus_mass_fg.get(pred_v6, 0.0001)  # virus mass (fg)
    S = device_sensitivity_fg.get(data.device_id, 1200)  # device sensitivity (fg)
    f0 = data.base_frequency_hz

    delta_m = S
    delta_f = f0 * (delta_m / m)
    drift = abs(data.measured_frequency_hz - f0)

    # Top‑5 predictions
    top5 = sorted(
        [
            {
                "virus_id": i + 1,
                "name": virus_names.get(i + 1, "Unknown"),
                "prob": p
            }
            for i, p in enumerate(probs_v6)
        ],
        key=lambda x: x["prob"],
        reverse=True
    )[:5]

    # Mass array aligned with probability array (index 0 → virus 1, etc.)
    virus_masses_aligned = [virus_mass_fg[i + 1] for i in range(len(probs_v6))]

    # Virus ID array for the frontend charts
    virus_ids = list(range(1, len(probs_v6) + 1))

    return {
        "model": "multi",
        "device_id": data.device_id,
        "virus_name": virus_names.get(pred_v6, "Unknown"),
        "virus_id": pred_v6,
        "probabilities": probs_v6,
        "virus_ids": virus_ids,
        "virus_masses_fg": virus_masses_aligned,
        "top_5": top5,
        "physics": {
            "virus_mass_fg": m,
            "device_sensitivity_fg": S,
            "delta_m_fg": delta_m,
            "delta_f_hz": delta_f,
            "delta_f_over_f": delta_f / f0,
            "delta_m_over_m": delta_m / m
        },
        "drift_hz": drift,
        "drift_flag": drift > 1.0
    }
