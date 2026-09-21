# app/routers/analyzer_v2.py

import logging
from fastapi import APIRouter, HTTPException
from app.schemas.analyzer_v2_schema import AnalyzerV2Request, AnalyzerV2Response
from app.services.analyzer_v2_service import (
    analyze_v2,
    get_all_devices_v2,
    get_device_v2,
    get_all_outputs_v2,
    get_output_v2,
    get_full_device_data_v2,
    compute_values_v2
)

router = APIRouter(prefix="/analyzer_v2", tags=["Analyzer v2"])
logger = logging.getLogger("analyzers")


@router.post("/", response_model=AnalyzerV2Response)
async def analyze_v2_endpoint(payload: AnalyzerV2Request):
    logger.info(f"[Analyzer v2] analyze_v2 called with payload={payload.dict()}")
    try:
        result = analyze_v2(payload)
        logger.info(f"[Analyzer v2] Analysis completed: {result}")
        return result
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in analyze_v2: {str(e)}")
        raise HTTPException(status_code=500, detail="Analyzer v2 failed")


@router.get("/devices")
async def get_all_devices_endpoint():
    logger.info("[Analyzer v2] get_all_devices called")
    try:
        return get_all_devices_v2()
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in get_all_devices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch devices")


@router.get("/devices/{device_id}")
async def get_device_endpoint(device_id: str):
    logger.info(f"[Analyzer v2] get_device called for device_id={device_id}")
    try:
        return get_device_v2(device_id)
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in get_device: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch device")


@router.get("/outputs")
async def get_all_outputs_endpoint():
    logger.info("[Analyzer v2] get_all_outputs called")
    try:
        return get_all_outputs_v2()
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in get_all_outputs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch outputs")


@router.get("/outputs/{device_id}")
async def get_output_endpoint(device_id: str):
    logger.info(f"[Analyzer v2] get_output called for device_id={device_id}")
    try:
        return get_output_v2(device_id)
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in get_output: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch output")


@router.get("/device_full/{device_id}")
async def get_full_device_data_endpoint(device_id: str):
    logger.info(f"[Analyzer v2] get_full_device_data called for device_id={device_id}")
    try:
        return get_full_device_data_v2(device_id)
    except Exception as e:
        logger.error(f"[Analyzer v2] ERROR in get_full_device_data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch outputs")
