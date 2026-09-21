from pydantic import BaseModel

class Analyzer1Request(BaseModel):
    id: int
    analyte: str
    concentration: float
    frequency_mhz: float
    af_mhz: float
    mass_g: float
