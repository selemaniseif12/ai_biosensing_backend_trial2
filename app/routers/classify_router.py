# ---------------------------------------------------------
# 100‑Virus Classifier V2 (Corrected + HuggingFace Loader)
# ---------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import numpy as np
import random

from app.database import get_db
from app.utils.token_utils import is_any_valid_token

# ⭐ Correct HuggingFace loader
from app.core.model_loader import (
    load_model_with_fallback,
    V2_LOCAL_PATH
)

router = APIRouter(tags=["100‑Virus Dashboard"])

# ---------------------------------------------------------
# Load V2 model ONCE using HuggingFace fallback
# ---------------------------------------------------------
model_v2 = load_model_with_fallback("VIRUS_MODEL_V2_URL", V2_LOCAL_PATH)


# ---------------------------------------------------------
# Virus metadata (names + masses)
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
# Threshold filter
# ---------------------------------------------------------
def apply_threshold_filter(results: dict[int, float], threshold_hz: float):
    if threshold_hz <= 0.1:
        return results
    return {k: v for k, v in results.items() if v >= threshold_hz}


# ---------------------------------------------------------
# V2 Request Model
# ---------------------------------------------------------
class V2ClassifyRequest(BaseModel):
    base_frequency_hz: float
    threshold_hz: float  # user provides threshold deviation


# ---------------------------------------------------------
# GET /classify/v2 — simple status check
# ---------------------------------------------------------
@router.get("/classify/v2")
def get_v2_status():
    return {"status": "V2 classifier online", "model_version": "v2"}


# ---------------------------------------------------------
# GET /classifier — general classifier status
# ---------------------------------------------------------
@router.get("/classifier")
def classifier_status():
    return {
        "v2": "online",
        "model_loaded": model_v2 is not None,
        "message": "Classifier system operational"
    }


# ---------------------------------------------------------
# GET /simulate — patented base frequency
# ---------------------------------------------------------
@router.get("/simulate")
def simulate_get():
    base = 1693999.26434753749357  # <-- YOUR PATENTED VALUE
    measured = base + random.uniform(-1.0, 1.0)

    return {
        "base_frequency_hz": base,
        "measured_frequency_hz": measured,
        "message": "Simulation generated using patented base frequency"
    }


# ---------------------------------------------------------
# Simulation Request Model
# ---------------------------------------------------------
class SimulationRequest(BaseModel):
    threshold_hz: float
    base_frequency_hz: float | None = None  # optional override


# ---------------------------------------------------------
# POST /simulate — measured = base + threshold
# ---------------------------------------------------------
@router.post("/simulate")
def simulate_post(req: SimulationRequest):
    if req.base_frequency_hz is not None:
        base = req.base_frequency_hz
    else:
        base = 1693999.26434753749357  # <-- YOUR PATENTED VALUE

    measured = base + req.threshold_hz

    return {
        "base_frequency_hz": base,
        "measured_frequency_hz": measured,
        "threshold_hz": req.threshold_hz,
        "message": "Simulation accepted using scientific deviation model"
    }


# ---------------------------------------------------------
# POST /classify/v2 — measured = base + threshold (scientific model)
# ---------------------------------------------------------
@router.post("/classify/v2")
def classify_v2(req: V2ClassifyRequest, token: str = Query(...), db: Session = Depends(get_db)):

    if not is_any_valid_token(db, token, ["ml_v2"]):
        raise HTTPException(status_code=403, detail="Invalid or inactive ML v2 token")

    # ⭐ Scientific rule:
    # measured frequency = base frequency + threshold deviation
    measured_frequency = req.base_frequency_hz + req.threshold_hz

    # ⭐ Build the exact 8‑feature vector used during training
    X = [
        req.base_frequency_hz,
        req.base_frequency_hz * 2,
        req.base_frequency_hz * 3,
        req.base_frequency_hz * 4,
        req.base_frequency_hz * 5,
        req.base_frequency_hz * 6,
        measured_frequency,
        5000.0
    ]

    probs = model_v2.predict_proba([X])[0]
    classes = model_v2.classes_

    # Dict: {virus_id: probability}
    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}

    # Sort by probability
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    # Apply threshold deviation filter
    filtered_results = apply_threshold_filter(sorted_results, req.threshold_hz)

    # Masses
    sorted_masses = {k: masses.get(k) for k in filtered_results.keys()}

    # Chart data
    chart_data = [
        {"virus_id": int(k), "probability": float(filtered_results[k]), "mass_fg": sorted_masses[k]}
        for k in filtered_results.keys()
    ]

    return {
        "model_version": "v2",
        "threshold_hz": req.threshold_hz,
        "base_frequency_hz": req.base_frequency_hz,
        "measured_frequency_hz": measured_frequency,
        "results": filtered_results,
        "virus_masses_fg": sorted_masses,
        "virus_names": {k: virus_names[k] for k in filtered_results.keys()},
        "chart_data": chart_data,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "100‑virus classification (V2) completed using scientific deviation model"
    }
