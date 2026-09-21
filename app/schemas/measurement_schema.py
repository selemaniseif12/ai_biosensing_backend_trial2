from pydantic import BaseModel
from typing import Optional


# ---------------------------------------------------------
# BASE SCHEMA
# ---------------------------------------------------------
class MeasurementBase(BaseModel):
    frequency_mhz: float
    delta_f_mhz: Optional[float] = None
    m_g: Optional[float] = None


# ---------------------------------------------------------
# CREATE SCHEMA (used for POST)
# ---------------------------------------------------------
class MeasurementCreate(MeasurementBase):
    sample_id: int
    device_id: int


# ---------------------------------------------------------
# RESPONSE SCHEMA (returned to client)
# ---------------------------------------------------------
class MeasurementResponse(MeasurementBase):
    id: int
    sample_id: int
    device_id: int

    class Config:
        from_attributes = True
