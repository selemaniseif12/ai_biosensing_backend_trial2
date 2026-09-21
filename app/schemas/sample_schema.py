# app/schemas/sample_schema.py

from pydantic import BaseModel
from datetime import datetime

class SampleBase(BaseModel):
    customer_id: str
    sample_type: str
    description: str | None = None
    created_at: datetime

class SampleCreate(SampleBase):
    pass

class SampleResponse(SampleBase):
    id: str
