# app/services/analyzer_v6_service.py

import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any

import joblib
import numpy as np

from .analyzer_v5_service import run_analyzer_v5

logger = logging.getLogger("analyzers")

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_PATH = Path(__file__).resolve().parent.parent
MODEL_BASE_PATH = BASE_PATH / "ml" / "models"


# ---------------------------------------------------------
# LOAD PER-DEVICE MODEL (CACHED)
# ---------------------------------------------------------
@lru_cache(maxsize=None)
def _load_v6_model(device_id: int):
    """
    Loads a per-device ML model for time-to-detection.
    Expected path pattern:
        ml/models/device_{device_id}_v6_time_model.joblib
    """

    model_path = MODEL_BASE_PATH / f"device_{device_id}_v6_time_model.joblib"
    logger.info(f"[Analyzer v6] Loading model for device_id={device_id}")

    try:
        if not model_path.exists():
            logger.error(f"[Analyzer v6] Model not found: {model_path}")
            raise FileNotFoundError(
                f"V6 time-to-detection model not found for device {device_id}: {model_path}"
            )

        model = joblib.load(model_path)
        logger.info(f"[Analyzer v6] Model loaded successfully for device_id={device_id}")
        return model

    except Exception as e:
        logger.error(f"[Analyzer v6] ERROR loading model for device_id={device_id}: {str(e)}")
        raise


# ---------------------------------------------------------
# MAIN ANALYZER V6
# ---------------------------------------------------------
def run_analyzer_v6(
    device_id: int,
    virus_id: int,
    deposition_rate: float,
    temperature: float | None = None,
    humidity: float | None = None,
    flow_rate: float | None = None,
) -> Dict[str, Any]:
    """
    Hybrid analyzer:
    - Uses V5 physics to compute required virus count and Δf
    - Uses ML model to estimate time-to-detection based on deposition rate and environment
    """

    logger.info(
        f"[Analyzer v6] run_analyzer_v6 called with "
        f"device_id={device_id}, virus_id={virus_id}, deposition_rate={deposition_rate}, "
        f"temperature={temperature}, humidity={humidity}, flow_rate={flow_rate}"
    )

    try:
        if deposition_rate <= 0:
            logger.error("[Analyzer v6] deposition_rate must be positive")
            raise ValueError("deposition_rate must be positive.")

        # ---------------- Physics Layer (v5) ----------------
        physics_result = run_analyzer_v5(device_id=device_id, virus_id=virus_id)

        # ---------------- ML Model Layer --------------------
        model = _load_v6_model(device_id)

        features = [
            physics_result["required_virus_count"],
            physics_result["virus_mass_fg"],
            physics_result["device_mass_resolution_g"],
            physics_result["delta_f_MHz"],
            deposition_rate,
            temperature if temperature is not None else 25.0,
            humidity if humidity is not None else 50.0,
            flow_rate if flow_rate is not None else 1.0,
        ]

        X = np.array(features, dtype=float).reshape(1, -1)
        time_to_detection = float(model.predict(X)[0])

        result = {
            **physics_result,
            "deposition_rate": deposition_rate,
            "temperature": temperature,
            "humidity": humidity,
            "flow_rate": flow_rate,
            "time_to_detection_seconds": time_to_detection,
        }

        logger.info(f"[Analyzer v6] Final result: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v6] ERROR in run_analyzer_v6: {str(e)}")
        raise
