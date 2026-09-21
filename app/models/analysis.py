# app/models/analysis.py

from pydantic import BaseModel
from datetime import datetime

class Analysis(BaseModel):
    id: str
    measurement_id: str
    sample_id: str
    customer_id: str
    classification: str
    confidence: float
    timestamp: datetime
    analyzer_version: str
