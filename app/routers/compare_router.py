from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np

# Import V2 + V6 routers (new versions)
from app.routers.classify_router import classify_v2
from app.routers.ml_multiclassify_router import ml_multiclassify_v6

# Token + DB imports
from app.database import get_db
from app.utils.token_utils import is_token_active

router = APIRouter(tags=["ML Compare"])

# ---------------------------------------------------------
# REQUIRE V6 TOKEN
# ---------------------------------------------------------
def require_v6_token(token: str, db: Session = Depends(get_db)):
    if is_token_active(db, token, "v6"):
        return True
    raise HTTPException(status_code=403, detail="V6 token required")

# ---------------------------------------------------------
# VIRUS NAMES + MASSES (same dictionaries used in V2/V6 routers)
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
# THRESHOLD FILTER
# ---------------------------------------------------------
def apply_threshold_filter(sorted_results: dict[int, float], threshold_hz: float):
    if threshold_hz <= 0:
        return sorted_results
    return {k: v for k, v in sorted_results.items() if v >= threshold_hz}

# ---------------------------------------------------------
# COMPARE V2 vs V6 — ONLINE MODE
# ---------------------------------------------------------
@router.post("/compare")
def compare_v2_v6(
    payload: dict,
    _ = Depends(require_v6_token),
    db: Session = Depends(get_db)
):
    features = payload.get("features")
    threshold_hz = payload.get("threshold_hz", 0.0)

    if not features:
        raise HTTPException(status_code=400, detail="Missing 'features' in payload")

    # -------------------------------
    # RUN V2 MODEL (using new router)
    # -------------------------------
    v2_response = classify_v2(
        type("obj", (object,), {"features": features, "threshold_hz": threshold_hz})
    )

    # -------------------------------
    # RUN V6 MODEL (using new router)
    # -------------------------------
    v6_response = classify_v6(
        type("obj", (object,), {"features": features, "threshold_hz": threshold_hz})
    )

    # -------------------------------
    # BUILD RESPONSE
    # -------------------------------
    return {
        "status": "success",
        "threshold_hz": threshold_hz,

        "v2": {
            "top_virus": virus_names[v2_response["top_prediction"]],
            "top_probability": v2_response["virus_probabilities"][v2_response["top_prediction"]],
            "results": [
                {
                    "virus_id": k,
                    "virus_name": virus_names[k],
                    "mass": masses[k],
                    "probability": v
                }
                for k, v in v2_response["virus_probabilities"].items()
            ]
        },

        "v6": {
            "top_virus": virus_names[v6_response["top_prediction"]],
            "top_probability": v6_response["virus_probabilities"][v6_response["top_prediction"]],
            "results": [
                {
                    "virus_id": k,
                    "virus_name": virus_names[k],
                    "mass": masses[k],
                    "probability": v
                }
                for k, v in v6_response["virus_probabilities"].items()
            ]
        }
    }
