# app/schemas/analysis_schema.py

from pydantic import BaseModel
from datetime import datetime

class AnalysisResponse(BaseModel):
    id: str
    measurement_id: str
    sample_id: str
    customer_id: str
    classification: str
    confidence: float
    timestamp: datetime
    analyzer_version: str
