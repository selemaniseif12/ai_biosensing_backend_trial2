from fastapi import APIRouter, HTTPException
from app.analyzers.analyzer_v6 import analyze_v6

router = APIRouter(
    prefix="/analyze",
    tags=["Analyzer"]
)

@router.post("/v6")
def analyze_v6_endpoint(payload: dict):
    data = payload.get("data")

    if data is None:
        raise HTTPException(status_code=400, detail="Missing 'data' field")

    return analyze_v6(data)
