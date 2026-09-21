import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from app.services.analyzer_orchestrator import orchestrate_analysis

router = APIRouter(
    prefix="/orchestrate",
    tags=["Analyzer Orchestrator"]
)

logger = logging.getLogger("analyzers")


class OrchestratorRequest(BaseModel):
    sensor_data: Optional[List[float]] = None
    device_id: Optional[int] = Field(None, ge=1, le=5)
    virus_id: Optional[int] = Field(None, ge=1, le=100)
    deposition_rate: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    flow_rate: Optional[float] = None


@router.post("/")
async def orchestrate(payload: OrchestratorRequest):
    logger.info(f"[Orchestrator] Request received: {payload.dict()}")

    try:
        result = await orchestrate_analysis(payload)
        return result

    except Exception as e:
        logger.error(f"[Orchestrator] ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
