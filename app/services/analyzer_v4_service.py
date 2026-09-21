# app/services/analyzer_v4_service.py

import logging
from pathlib import Path
from typing import List, Dict, Any

import joblib
import numpy as np
import xgboost as xgb

logger = logging.getLogger("analyzers")

# ---------------------------------------------------------
# MODEL LOADING (done once at startup)
# ---------------------------------------------------------

try:
    BASE_PATH = Path(__file__).resolve().parent.parent / "ml" / "models"

    RF_MODEL_PATH = BASE_PATH / "qcm_virus_classifier_rf.joblib"
    XGB_MODEL_PATH = BASE_PATH / "qcm_virus_classifier_xgb.json"
    LABEL_ENCODER_PATH = BASE_PATH / "qcm_virus_label_encoder.joblib"

    rf_model = joblib.load(RF_MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)

    xgb_booster = xgb.Booster()
    xgb_booster.load_model(str(XGB_MODEL_PATH))

    logger.info("[Analyzer v4] RF model, XGB booster, and label encoder loaded successfully")

except Exception as e:
    logger.error(f"[Analyzer v4] ERROR loading models or encoder: {str(e)}")
    raise


# ---------------------------------------------------------
# Helper: run XGBoost and get probabilities
# ---------------------------------------------------------
def _xgb_predict_proba(features: np.ndarray) -> np.ndarray:
    """
    Runs XGBoost booster on a single sample and returns class probabilities.
    features: shape (n_features,)
    returns: shape (n_classes,)
    """

    try:
        dmatrix = xgb.DMatrix(features.reshape(1, -1))
        probs = xgb_booster.predict(dmatrix)[0]
        return probs

    except Exception as e:
        logger.error(f"[Analyzer v4] ERROR in _xgb_predict_proba: {str(e)}")
        raise


# ---------------------------------------------------------
# Main hybrid analyzer v4
# ---------------------------------------------------------
def run_analyzer_v4(sensor_data: List[float]) -> Dict[str, Any]:
    """
    Hybrid analyzer:
    - Runs Random Forest and XGBoost
    - Averages their probability distributions
    - Returns final label + per-model details
    """

    logger.info(f"[Analyzer v4] run_analyzer_v4 called with {len(sensor_data)} data points")

    try:
        if not sensor_data or len(sensor_data) == 0:
            logger.warning("[Analyzer v4] Empty sensor_data received")
            return {
                "input_length": 0,
                "final_prediction_label": "invalid",
                "final_prediction_confidence": 0.0,
                "message": "No sensor data provided."
            }

        # Convert input to numpy array
        x = np.array(sensor_data, dtype=float)

        # ---------------- RF prediction ----------------
        rf_probs = rf_model.predict_proba([x])[0]
        rf_class_index = int(np.argmax(rf_probs))
        rf_confidence = float(rf_probs[rf_class_index])

        # ---------------- XGB prediction ---------------
        xgb_probs = _xgb_predict_proba(x)
        xgb_class_index = int(np.argmax(xgb_probs))
        xgb_confidence = float(xgb_probs[xgb_class_index])

        # ---------------- Hybrid (average) -------------
        hybrid_probs = (rf_probs + xgb_probs) / 2.0
        hybrid_class_index = int(np.argmax(hybrid_probs))
        hybrid_confidence = float(hybrid_probs[hybrid_class_index])

        # Decode class indices → labels
        rf_label = label_encoder.inverse_transform([rf_class_index])[0]
        xgb_label = label_encoder.inverse_transform([xgb_class_index])[0]
        hybrid_label = label_encoder.inverse_transform([hybrid_class_index])[0]

        result = {
            "input_length": len(sensor_data),

            "rf": {
                "class_index": rf_class_index,
                "label": rf_label,
                "confidence": rf_confidence,
                "probabilities": rf_probs.tolist(),
            },

            "xgb": {
                "class_index": xgb_class_index,
                "label": xgb_label,
                "confidence": xgb_confidence,
                "probabilities": xgb_probs.tolist(),
            },

            "hybrid": {
                "class_index": hybrid_class_index,
                "label": hybrid_label,
                "confidence": hybrid_confidence,
                "probabilities": hybrid_probs.tolist(),
            },

            "final_prediction_label": hybrid_label,
            "final_prediction_confidence": hybrid_confidence,
        }

        logger.info(f"[Analyzer v4] Hybrid analysis result: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v4] ERROR in run_analyzer_v4: {str(e)}")
        raise
