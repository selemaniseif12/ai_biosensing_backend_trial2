# app/routers/analyzer_v6.py

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.analyzer_v6_service import run_analyzer_v6

router = APIRouter(
    prefix="/analyzer_v6",
    tags=["Analyzer v6"]
)

logger = logging.getLogger("analyzers")


class AnalyzerV6Request(BaseModel):
    device_id: int = Field(..., ge=1, le=5)
    virus_id: int = Field(..., ge=1, le=100)
    deposition_rate: float = Field(..., gt=0)
    temperature: float | None = None
    humidity: float | None = None
    flow_rate: float | None = None


class AnalyzerV6Response(BaseModel):
    device_id: int
    virus_id: int
    virus: str
    virus_mass_fg: float
    device_mass_resolution_g: float
    required_virus_count: int
    f_MHz: float
    delta_f_MHz: float
    binding_profile: str
    deposition_rate: float
    temperature: float | None
    humidity: float | None
    flow_rate: float | None
    time_to_detection_seconds: float


@router.post("/", response_model=AnalyzerV6Response)
def analyze_v6(request: AnalyzerV6Request):
    logger.info(
        f"[Analyzer v6] analyze_v6 called with "
        f"device_id={request.device_id}, virus_id={request.virus_id}, "
        f"deposition_rate={request.deposition_rate}, "
        f"temperature={request.temperature}, humidity={request.humidity}, "
        f"flow_rate={request.flow_rate}"
    )

    try:
        result = run_analyzer_v6(
            device_id=request.device_id,
            virus_id=request.virus_id,
            deposition_rate=request.deposition_rate,
            temperature=request.temperature,
            humidity=request.humidity,
            flow_rate=request.flow_rate,
        )

        logger.info(f"[Analyzer v6] Analysis completed: {result}")
        return AnalyzerV6Response(**result)

    except Exception as e:
        logger.error(f"[Analyzer v6] ERROR in analyze_v6: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
