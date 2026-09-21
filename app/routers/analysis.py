from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.services.analysis_service import (
    list_analysis,
    get_analysis,
    get_analysis_for_sample,
    get_analysis_for_customer,
    get_analysis_for_measurement,
    get_analysis_by_date_range,
    get_analysis_for_analyzer_version,
    get_analysis_for_virus,
    get_analysis_for_device,
    get_analysis_combined,
    sort_analysis_newest_first,
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

# ---------------------------------------------------------
# LIST ALL ANALYSIS (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/")
def list_all_analysis_route():
    try:
        entries = list_analysis()
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# GET ANALYSIS FOR SAMPLE (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/sample/{sample_id}")
def get_analysis_for_sample_route(sample_id: str):
    try:
        entries = get_analysis_for_sample(sample_id)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# GET ANALYSIS FOR CUSTOMER (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/customer/{customer_id}")
def get_analysis_for_customer_route(customer_id: str):
    try:
        entries = get_analysis_for_customer(customer_id)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# GET ANALYSIS FOR MEASUREMENT (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/measurement/{measurement_id}")
def get_analysis_for_measurement_route(measurement_id: str):
    try:
        entries = get_analysis_for_measurement(measurement_id)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# FILTER ANALYSIS BY DATE RANGE (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/date-range")
def get_analysis_by_date_range_route(start: datetime, end: datetime):
    try:
        if start > end:
            raise HTTPException(status_code=400, detail="start date must be <= end date")
        entries = get_analysis_by_date_range(start, end)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# FILTER ANALYSIS BY ANALYZER VERSION (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/analyzer/{version}")
def get_analysis_for_analyzer_version_route(version: str):
    try:
        entries = get_analysis_for_analyzer_version(version)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# FILTER ANALYSIS BY VIRUS TYPE (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/virus/{virus}")
def get_analysis_for_virus_route(virus: str):
    try:
        entries = get_analysis_for_virus(virus)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# FILTER ANALYSIS BY DEVICE ID (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/device/{device_id}")
def get_analysis_for_device_route(device_id: str):
    try:
        entries = get_analysis_for_device(device_id)
        return sort_analysis_newest_first(entries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# COMBINED FILTER: DEVICE + VIRUS + DATE RANGE (NEWEST FIRST)
# ---------------------------------------------------------
@router.get("/combined")
def get_analysis_combined_route(
    device_id: str,
    virus: str,
    start: datetime,
    end: datetime
):
    try:
        if start > end:
            raise HTTPException(status_code=400, detail="start date must be <= end date")

        entries = get_analysis_combined(device_id, virus, start, end)
        return sort_analysis_newest_first(entries)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# GET ANALYSIS BY ID
# ---------------------------------------------------------
@router.get("/{analysis_id}")
def get_analysis_by_id_route(analysis_id: str):
    try:
        result = get_analysis(analysis_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
