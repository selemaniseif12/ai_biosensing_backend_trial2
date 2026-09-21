from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np
import random

router = APIRouter()

# ---------------------------------------------------------
# TOKEN VERIFICATION
# ---------------------------------------------------------
def verify_token(token: str):
    expected_token = os.getenv("API_TOKEN")
    if expected_token and token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# ---------------------------------------------------------
# MODEL PATHS (corrected)
# ---------------------------------------------------------
MODEL_V2_PATH = "app/models/sim_model_v2_100.pkl"
MODEL_V6_PATH = "app/models/sim_model_v6_100.pkl"

model_v2 = None
model_v6 = None

def load_models():
    global model_v2, model_v6

    if model_v2 is None:
        if os.path.exists(MODEL_V2_PATH):
            model_v2 = joblib.load(MODEL_V2_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V2_PATH}")

    if model_v6 is None:
        if os.path.exists(MODEL_V6_PATH):
            model_v6 = joblib.load(MODEL_V6_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V6_PATH}")

# ---------------------------------------------------------
# VIRUS NAMES + MASSES (1–100)
# ---------------------------------------------------------
virus_names = {
    1: "COVID‑19 (SARS‑CoV‑2)", 2: "Influenza A (H1N1)", 3: "Influenza A (H3N2)",
    4: "Influenza B", 5: "SARS‑CoV‑1", 6: "MERS‑CoV", 7: "RSV‑A", 8: "RSV‑B",
    9: "Rhinovirus A", 10: "Rhinovirus B", 11: "Rhinovirus C", 12: "Adenovirus 3",
    13: "Adenovirus 5", 14: "Adenovirus 7", 15: "Parainfluenza 1",
    16: "Parainfluenza 2", 17: "Parainfluenza 3", 18: "Parainfluenza 4",
    19: "Human Metapneumovirus", 20: "Measles virus", 21: "Mumps virus",
    22: "Rubella virus", 23: "Varicella‑Zoster", 24: "Cytomegalovirus",
    25: "Epstein‑Barr virus", 26: "Human Bocavirus", 27: "Enterovirus D68",
    28: "Enterovirus A71", 29: "Hantavirus", 30: "Lassa virus",
    31: "Nipah virus", 32: "Hendra virus", 33: "SARS‑CoV‑2 Omicron",
    34: "SARS‑CoV‑2 Delta", 35: "SARS‑CoV‑2 Alpha", 36: "SARS‑CoV‑2 Beta",
    37: "SARS‑CoV‑2 Gamma", 38: "Human Coronavirus 229E",
    39: "Human Coronavirus NL63", 40: "Human Coronavirus OC43",
    41: "Human Coronavirus HKU1", 42: "Influenza C", 43: "Influenza D",
    44: "Human Parechovirus", 45: "Human Polyomavirus",
    46: "Human Mastadenovirus C", 47: "Human Mastadenovirus B",
    48: "Human Mastadenovirus E", 49: "Human Astrovirus",
    50: "Norovirus GII", 51: "Norovirus GI", 52: "Rotavirus A",
    53: "Rotavirus B", 54: "Rotavirus C", 55: "Human Reovirus",
    56: "Human Orthopneumovirus", 57: "Human Respirovirus",
    58: "Human Rubulavirus", 59: "Human Morbillivirus",
    60: "Human Alphavirus", 61: "Human Betacoronavirus",
    62: "Human Gammacoronavirus", 63: "Human Deltacoronavirus",
    64: "Avian Influenza H5N1", 65: "Avian Influenza H7N9",
    66: "Avian Influenza H9N2", 67: "Canine Influenza H3N8",
    68: "Swine Influenza H1N2", 69: "Swine Influenza H3N2",
    70: "Human Enterovirus C", 71: "Human Enterovirus B",
    72: "Human Enterovirus A", 73: "Human Coxsackievirus A",
    74: "Human Coxsackievirus B", 75: "Human Echovirus",
    76: "Human Parechovirus 3", 77: "Human Orthobunyavirus",
    78: "Human Phlebovirus", 79: "Human Arenavirus",
    80: "Human Bornavirus", 81: "Human Torovirus",
    82: "Hepatitis A (airborne rare)", 83: "Hepatitis E (airborne rare)",
    84: "Human Polyomavirus KI", 85: "Human Polyomavirus WU",
    86: "Human Parvovirus B19", 87: "Torque Teno Virus",
    88: "Human Sapovirus", 89: "Human Aichivirus",
    90: "Human Cardiovirus", 91: "Human Kobuvirus",
    92: "Human Salivirus", 93: "Human Cosavirus",
    94: "Human Orthoreovirus 3", 95: "Human Rotavirus H",
    96: "Human Astrovirus MLB", 97: "Human Astrovirus VA",
    98: "Human Adenovirus 14", 99: "Human Adenovirus 55",
    100: "Human Adenovirus 21"
}

masses = {
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
# THRESHOLD NORMALIZATION RULE
# ---------------------------------------------------------
def normalize_threshold(threshold_hz: float) -> float:
    if threshold_hz is None:
        return 0.1
    return float(threshold_hz)

# ---------------------------------------------------------
# V6 PHYSICS SIMULATION
# ---------------------------------------------------------
def generate_v6_features(base_frequency_hz: float):
    mass_sensitivity = 0.000001 + random.uniform(-0.0000003, 0.0000003)
    delta_m = 0.0001 + random.uniform(-0.00005, 0.00005)
    delta_m_over_m = delta_m / 1.0
    delta_f_hz = mass_sensitivity * base_frequency_hz * delta_m_over_m
    noise_hz = random.uniform(0.5, 5.0)
    measured_frequency_hz = base_frequency_hz + delta_f_hz + noise_hz
    quality_factor = 4990 + random.uniform(-50, 50)

    return [
        base_frequency_hz,
        mass_sensitivity,
        delta_m,
        delta_m_over_m,
        delta_f_hz,
        noise_hz,
        measured_frequency_hz,
        quality_factor
    ], {
        "base_frequency_hz": base_frequency_hz,
        "mass_sensitivity": mass_sensitivity,
        "delta_m": delta_m,
        "delta_m_over_m": delta_m_over_m,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,
        "measured_frequency_hz": measured_frequency_hz,
        "quality_factor": quality_factor
    }

# ---------------------------------------------------------
# THRESHOLD FILTERING
# ---------------------------------------------------------
def apply_threshold_filter(sorted_results: dict[int, float], threshold_hz: float):
    if threshold_hz <= 0.1:
        return sorted_results
    return {k: v for k, v in sorted_results.items() if v >= threshold_hz}

# ---------------------------------------------------------
# GET /v6/simulation
# ---------------------------------------------------------
@router.get("/v6/simulation")
def get_v6_simulation(base_frequency_hz: float,
                      token: str = Depends(verify_token)):

    features, physics = generate_v6_features(base_frequency_hz)

    return {
        "model_version": "v6",
        "input_base_frequency_hz": base_frequency_hz,
        "physics": physics,
        "message": "V6 physics simulation generated."
    }

# ---------------------------------------------------------
# GET /v6/classify
# ---------------------------------------------------------
@router.get("/v6/classify")
def get_v6_classify(base_frequency_hz: float,
                    threshold_hz: float = 0.1,
                    token: str = Depends(verify_token)):

    threshold_hz = normalize_threshold(threshold_hz)
    load_models()

    features, physics = generate_v6_features(base_frequency_hz)
    probs = model_v6.predict_proba([features])[0]
    classes = model_v6.classes_

    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    filtered_results = apply_threshold_filter(sorted_results, threshold_hz)

    filtered_names = {k: virus_names.get(k) for k in filtered_results.keys()}
    filtered_masses = {k: masses.get(k) for k in filtered_results.keys()}

    return {
        "model_version": "v6",
        "threshold_hz": threshold_hz,
        "input_base_frequency_hz": base_frequency_hz,
        **physics,
        "results": filtered_results,
        "virus_names": filtered_names,
        "virus_masses_fg": filtered_masses,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "V6 classification completed (GET)."
    }

# ---------------------------------------------------------
# GET /v6/classifier
# ---------------------------------------------------------
@router.get("/v6/classifier")
def get_v6_classifier(token: str = Depends(verify_token)):
    load_models()

    return {
        "model_version": "v6",
        "classes": list(map(int, model_v6.classes_)),
        "virus_names": virus_names,
        "virus_masses_fg": masses,
        "message": "V6 classifier metadata."
    }

# ---------------------------------------------------------
# POST /v6/simulation
# ---------------------------------------------------------
class V6SimRequest(BaseModel):
    base_frequency_hz: float

@router.post("/v6/simulation")
def post_v6_simulation(req: V6SimRequest,
                       token: str = Depends(verify_token)):

    features, physics = generate_v6_features(req.base_frequency_hz)

    return {
        "model_version": "v6",
        "input_base_frequency_hz": req.base_frequency_hz,
        "physics": physics,
        "message": "V6 physics simulation generated (POST)."
    }

# ---------------------------------------------------------
# POST /classify/v6
# ---------------------------------------------------------
class V6Request(BaseModel):
    base_frequency_hz: float
    threshold_hz: float = 0.1

@router.post("/classify/v6")
def classify_v6(req: V6Request,
                token: str = Depends(verify_token)):

    req.threshold_hz = normalize_threshold(req.threshold_hz)
    load_models()

    features, physics = generate_v6_features(req.base_frequency_hz)
    probs = model_v6.predict_proba([features])[0]
    classes = model_v6.classes_

    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    filtered_results = apply_threshold_filter(sorted_results, req.threshold_hz)

    filtered_names = {k: virus_names.get(k) for k in filtered_results.keys()}
    filtered_masses = {k: masses.get(k) for k in filtered_results.keys()}

    return {
        "model_version": "v6",
        "threshold_hz": req.threshold_hz,
        "input_base_frequency_hz": req.base_frequency_hz,
        **physics,
        "results": filtered_results,
        "virus_names": filtered_names,
        "virus_masses_fg": filtered_masses,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "V6 classification completed using restored physics simulation."
    }

# ---------------------------------------------------------
# POST /classify/v2
# ---------------------------------------------------------
class SimpleClassifyRequest(BaseModel):
    features: list[float]
    threshold_hz: float = 0.1

@router.post("/classify/v2")
def classify_v2(req: SimpleClassifyRequest,
                token: str = Depends(verify_token)):

    req.threshold_hz = normalize_threshold(req.threshold_hz)
    load_models()

    probs = model_v2.predict_proba([req.features])[0]
    classes = model_v2.classes_

    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    filtered_results = apply_threshold_filter(sorted_results, req.threshold_hz)

    return {
        "model_version": "v2",
        "input_features": req.features,
        "threshold_hz": req.threshold_hz,
        "results": filtered_results,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "V2 classification completed."
    }
