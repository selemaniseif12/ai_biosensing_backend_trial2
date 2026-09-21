from pydantic import BaseModel
from typing import List, Optional

class AnalyzerV2Request(BaseModel):
    device_id: str
    data: List[float]

class AnalyzerV2Response(BaseModel):
    device_id: str
    features: List[float]
    prediction: Optional[str] = None
    confidence: Optional[float] = None
