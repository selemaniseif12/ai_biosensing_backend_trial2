# app/models/sample.py

from pydantic import BaseModel
from datetime import datetime

class Sample(BaseModel):
    id: str
    customer_id: str
    sample_type: str
    description: str | None = None
    created_at: datetime
