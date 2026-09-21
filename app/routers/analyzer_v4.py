# app/routers/analyzer_v4.py

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.measurement_service import get_measurement
from app.services.sample_service import get_sample
from app.services.customer_service import get_customer
from app.services.analysis_service import store_analysis

router = APIRouter(
    prefix="/analyzer_v4",
    tags=["Analyzer v4"]
)

logger = logging.getLogger("analyzers")


class AnalyzerV4Request(BaseModel):
    measurement_id: str


# ---------------------------------------------------------
# Analyzer v4 HTTP Endpoint
# ---------------------------------------------------------
@router.post("/")
def analyze_v4(request: AnalyzerV4Request):
    logger.info(f"[Analyzer v4] analyze_v4 called with measurement_id={request.measurement_id}")

    try:
        measurement = get_measurement(request.measurement_id)
        if not measurement:
            logger.error(f"[Analyzer v4] Measurement not found: {request.measurement_id}")
            raise HTTPException(status_code=404, detail="Measurement not found")

        sample = get_sample(measurement.sample_id)
        customer = get_customer(sample.customer_id)

        classification = "Staphylococcus aureus"
        confidence = 0.92

        result = {
            "measurement_id": measurement.id,
            "sample_id": sample.id,
            "customer_id": customer.id,
            "classification": classification,
            "confidence": confidence,
            "timestamp": datetime.utcnow(),
            "analyzer_version": "v4",
        }

        logger.info(f"[Analyzer v4] Analysis completed: {result}")
        return store_analysis(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Analyzer v4] ERROR in analyze_v4: {str(e)}")
        raise HTTPException(status_code=500, detail="Analyzer v4 failed")


# ---------------------------------------------------------
# Analyzer v4 Internal Function (used by unified analyzer)
# ---------------------------------------------------------
def run_analyzer_v4(metadata, signal):
    logger.info(f"[Analyzer v4] run_analyzer_v4 called for sample_id={metadata.sample_id}")

    try:
        customer = get_customer(metadata.customer_id)
        sample = get_sample(metadata.sample_id)
        measurement = get_measurement(metadata.sample_id)

        analyzer_output = {
            "version": "v4",
            "message": "Analyzer v4 executed",
            "timestamp": datetime.utcnow().isoformat(),
            "sample_id": metadata.sample_id,
            "customer_id": metadata.customer_id,
            "signal_points": len(signal.time),
        }

        ml_predictions = {
            "label": "positive",
            "probabilities": {"negative": 0.10, "positive": 0.90},
        }

        result = {
            "analyzer_output": analyzer_output,
            "ml_predictions": ml_predictions,
        }

        logger.info(f"[Analyzer v4] run_analyzer_v4 completed: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v4] ERROR in run_analyzer_v4: {str(e)}")
        raise
