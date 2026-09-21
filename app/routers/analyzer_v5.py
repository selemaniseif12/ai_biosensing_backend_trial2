# app/routers/analyzer_v5.py

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.analyzer_v5_service import run_analyzer_v5

router = APIRouter(
    prefix="/analyzer_v5",
    tags=["Analyzer v5"]
)

logger = logging.getLogger("analyzers")


class AnalyzerV5Request(BaseModel):
    device_id: int = Field(..., ge=1, le=5)
    virus_id: int = Field(..., ge=1, le=100)


class AnalyzerV5Response(BaseModel):
    device_id: int
    virus_id: int
    virus: str
    virus_mass_fg: float
    device_mass_resolution_g: float
    required_virus_count: int
    f_MHz: float
    delta_f_MHz: float
    binding_profile: str


@router.post("/", response_model=AnalyzerV5Response)
def analyze_v5(request: AnalyzerV5Request):
    logger.info(
        f"[Analyzer v5] analyze_v5 called with device_id={request.device_id}, virus_id={request.virus_id}"
    )

    try:
        result = run_analyzer_v5(
            device_id=request.device_id,
            virus_id=request.virus_id,
        )

        logger.info(f"[Analyzer v5] Analysis completed: {result}")
        return AnalyzerV5Response(**result)

    except Exception as e:
        logger.error(f"[Analyzer v5] ERROR in analyze_v5: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
