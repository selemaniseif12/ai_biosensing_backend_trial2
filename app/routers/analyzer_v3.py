# app/routers/analyzer_v3.py

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.measurement_service import get_measurement
from app.services.sample_service import get_sample
from app.services.customer_service import get_customer
from app.services.analysis_service import store_analysis

router = APIRouter(
    prefix="/analyzer_v3",
    tags=["Analyzer v3"]
)

logger = logging.getLogger("analyzers")


class AnalyzerV3Request(BaseModel):
    measurement_id: str


# ---------------------------------------------------------
# Analyzer v3 HTTP Endpoint
# ---------------------------------------------------------
@router.post("/")
def analyze_v3(request: AnalyzerV3Request):
    logger.info(f"[Analyzer v3] analyze_v3 called with measurement_id={request.measurement_id}")

    try:
        measurement = get_measurement(request.measurement_id)
        if not measurement:
            logger.error(f"[Analyzer v3] Measurement not found: {request.measurement_id}")
            raise HTTPException(status_code=404, detail="Measurement not found")

        sample = get_sample(measurement.sample_id)
        customer = get_customer(sample.customer_id)

        classification = "Listeria"
        confidence = 0.91

        result = {
            "measurement_id": measurement.id,
            "sample_id": sample.id,
            "customer_id": customer.id,
            "classification": classification,
            "confidence": confidence,
            "timestamp": datetime.utcnow(),
            "analyzer_version": "v3",
        }

        logger.info(f"[Analyzer v3] Analysis completed: {result}")
        return store_analysis(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Analyzer v3] ERROR in analyze_v3: {str(e)}")
        raise HTTPException(status_code=500, detail="Analyzer v3 failed")


# ---------------------------------------------------------
# Analyzer v3 Internal Function (used by unified analyzer)
# ---------------------------------------------------------
def run_analyzer_v3(metadata, signal):
    logger.info(f"[Analyzer v3] run_analyzer_v3 called for sample_id={metadata.sample_id}")

    try:
        customer = get_customer(metadata.customer_id)
        sample = get_sample(metadata.sample_id)
        measurement = get_measurement(metadata.sample_id)

        analyzer_output = {
            "version": "v3",
            "message": "Analyzer v3 executed",
            "timestamp": datetime.utcnow().isoformat(),
            "sample_id": metadata.sample_id,
            "customer_id": metadata.customer_id,
            "signal_points": len(signal.time),
        }

        ml_predictions = {
            "label": "negative",
            "probabilities": {"negative": 0.60, "positive": 0.40},
        }

        result = {
            "analyzer_output": analyzer_output,
            "ml_predictions": ml_predictions,
        }

        logger.info(f"[Analyzer v3] run_analyzer_v3 completed: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v3] ERROR in run_analyzer_v3: {str(e)}")
        raise
