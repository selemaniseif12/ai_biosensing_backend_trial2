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
# CREATE SCHEMA (POST)
# ---------------------------------------------------------
class MeasurementCreate(MeasurementBase):
    sample_id: int
    device_id: int


# ---------------------------------------------------------
# UPDATE SCHEMA (PATCH/PUT)
# ---------------------------------------------------------
class MeasurementUpdate(BaseModel):
    frequency_mhz: Optional[float] = None
    delta_f_mhz: Optional[float] = None
    m_g: Optional[float] = None


# ---------------------------------------------------------
# RESPONSE SCHEMA
# ---------------------------------------------------------
class MeasurementDB(MeasurementBase):
    id: int
    sample_id: int
    device_id: int

    class Config:
        from_attributes = True
