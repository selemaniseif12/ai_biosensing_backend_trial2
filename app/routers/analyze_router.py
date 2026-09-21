# app/routers/analyze.py

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

from app.services.analyzer_v1_service import run_analyzer_v1
from app.services.analyzer_v2_service import analyze_v2
from app.services.analyzer_v3_service import run_analyzer_v3
from app.services.analyzer_v4_service import run_analyzer_v4
from app.services.analyzer_v5_service import run_analyzer_v5
from app.services.analyzer_v6_service import run_analyzer_v6

router = APIRouter(prefix="/analyze", tags=["Unified Analyzer"])
logger = logging.getLogger("analyzers")


class UnifiedAnalyzeRequest(BaseModel):
    analyzer_version: Optional[
        Literal["v1", "v2", "v3", "v4", "v5", "v6", "auto"]
    ] = "auto"

    # For v1–v4
    sensor_data: Optional[List[float]] = None

    # For v5–v6
    device_id: Optional[int] = Field(None, ge=1, le=5)
    virus_id: Optional[int] = Field(None, ge=1, le=100)

    # For v6
    deposition_rate: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    flow_rate: Optional[float] = None


@router.post("/")
def unified_analyze(payload: UnifiedAnalyzeRequest):
    logger.info(f"[Unified Analyzer] Request received: {payload.dict()}")

    try:
        version = payload.analyzer_version

        # ------------------------------
        # AUTO-SELECTION LOGIC
        # ------------------------------
        if version == "auto":
            if payload.sensor_data:
                # ML analyzers
                if len(payload.sensor_data) > 50:
                    version = "v4"
                elif len(payload.sensor_data) > 20:
                    version = "v3"
                else:
                    version = "v1"
            elif payload.device_id and payload.virus_id:
                if payload.deposition_rate:
                    version = "v6"
                else:
                    version = "v5"
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient data for auto analyzer selection."
                )

        # ------------------------------
        # ROUTING TO ANALYZERS
        # ------------------------------
        if version == "v1":
            return {"version": "v1", "result": run_analyzer_v1(payload.sensor_data)}

        if version == "v2":
            return {"version": "v2", "result": analyze_v2(payload)}

        if version == "v3":
            return {"version": "v3", "result": run_analyzer_v3(payload.sensor_data)}

        if version == "v4":
            return {"version": "v4", "result": run_analyzer_v4(payload.sensor_data)}

        if version == "v5":
            return {
                "version": "v5",
                "result": run_analyzer_v5(payload.device_id, payload.virus_id)
            }

        if version == "v6":
            return {
                "version": "v6",
                "result": run_analyzer_v6(
                    device_id=payload.device_id,
                    virus_id=payload.virus_id,
                    deposition_rate=payload.deposition_rate,
                    temperature=payload.temperature,
                    humidity=payload.humidity,
                    flow_rate=payload.flow_rate,
                )
            }

        raise HTTPException(status_code=400, detail="Unsupported analyzer version.")

    except Exception as e:
        logger.error(f"[Unified Analyzer] ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
