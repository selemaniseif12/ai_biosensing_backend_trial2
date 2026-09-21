# app/services/analyzer_v1_service.py

import logging
from typing import List, Dict
import numpy as np

logger = logging.getLogger("analyzers")

# ---------------------------------------------------------
# ANALYZER V1 SERVICE
# ---------------------------------------------------------

def analyze_signal_v1(sensor_data: List[float], model_version: str = "v1") -> Dict:
    """
    Perform basic signal analysis for QCM biosensor data.
    This is a placeholder for your ML model integration.
    """

    logger.info(f"[Analyzer v1] analyze_signal_v1 called with {len(sensor_data)} data points")

    try:
        if not sensor_data or len(sensor_data) < 3:
            logger.warning("[Analyzer v1] Insufficient sensor data for analysis")
            return {
                "classification": "invalid",
                "confidence": 0.0,
                "model_version": model_version,
                "message": "Insufficient sensor data for analysis."
            }

        # Example: simple statistical analysis
        mean_val = float(np.mean(sensor_data))
        std_val = float(np.std(sensor_data))

        # Placeholder classification logic
        classification = "positive" if mean_val > std_val else "negative"
        confidence = round(
            abs(mean_val - std_val) / (mean_val + std_val + 1e-6), 3
        )

        result = {
            "classification": classification,
            "confidence": confidence,
            "model_version": model_version,
            "message": "Signal analyzed successfully."
        }

        logger.info(f"[Analyzer v1] Analysis result: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in analyze_signal_v1: {str(e)}")
        raise


def run_analyzer_v1(sensor_data: List[float], model_version: str = "v1") -> Dict:
    """
    Wrapper function for analyzer v1 — used by routers or services.
    Calls analyze_signal_v1 internally.
    """

    logger.info(f"[Analyzer v1] run_analyzer_v1 called (model_version={model_version})")

    try:
        result = analyze_signal_v1(sensor_data, model_version)
        result["status"] = "completed"

        logger.info(f"[Analyzer v1] run_analyzer_v1 completed: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in run_analyzer_v1: {str(e)}")
        raise
