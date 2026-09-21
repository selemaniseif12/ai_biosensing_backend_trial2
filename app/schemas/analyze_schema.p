from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    device_id: str
    payload: Dict[str, Any]
    preferred_analyzer: Optional[str] = None  # "v2", "v4", "v6", etc.


class AnalyzerResult(BaseModel):
    analyzer_version: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AnalyzeResponse(BaseModel):
    device_id: str
    analyzers_used: List[str]
    primary_analyzer: Optional[str]
    ml_prediction: Optional[str] = None
    ml_confidence: Optional[float] = None
    results: Dict[str, AnalyzerResult]
    timestamp: str
