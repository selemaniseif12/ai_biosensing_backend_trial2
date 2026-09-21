# app/models/measurement.py

from pydantic import BaseModel
from datetime import datetime

class Measurement(BaseModel):
    id: str
    sample_id: str
    frequency_data: list[float]
    timestamp: datetime
