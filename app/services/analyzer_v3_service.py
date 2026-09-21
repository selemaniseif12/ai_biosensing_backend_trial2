# app/services/analyzer_v3_service.py

import logging
import joblib
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger("analyzers")

# ---------------------------------------------------------
# MODEL LOADING (done once at startup)
# ---------------------------------------------------------

try:
    BASE_PATH = Path(__file__).resolve().parent.parent / "ml" / "models"

    MODEL_PATH = BASE_PATH / "qcm_virus_classifier_rf.joblib"
    LABEL_ENCODER_PATH = BASE_PATH / "qcm_virus_label_encoder.joblib"

    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)

    logger.info("[Analyzer v3] ML model and label encoder loaded successfully")

except Exception as e:
    logger.error(f"[Analyzer v3] ERROR loading model or encoder: {str(e)}")
    raise


# ---------------------------------------------------------
# ANALYZER V3 — MAIN PROCESSING
# ---------------------------------------------------------

def run_analyzer_v3(sensor_data: List[float]) -> Dict[str, Any]:
    """
    Runs the ML classifier on the provided sensor data.
    """

    logger.info(f"[Analyzer v3] run_analyzer_v3 called with {len(sensor_data)} data points")

    try:
        if not sensor_data or len(sensor_data) == 0:
            logger.warning("[Analyzer v3] Empty sensor_data received")
            return {
                "prediction_raw": None,
                "prediction_label": "invalid",
                "input_length": 0,
                "message": "No sensor data provided."
            }

        # ML model expects 2D array
        prediction = model.predict([sensor_data])[0]

        # Convert numeric class → label
        label = label_encoder.inverse_transform([prediction])[0]

        result = {
            "prediction_raw": int(prediction),
            "prediction_label": label,
            "input_length": len(sensor_data),
            "message": "Prediction completed successfully."
        }

        logger.info(f"[Analyzer v3] Prediction result: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v3] ERROR in run_analyzer_v3: {str(e)}")
        raise
