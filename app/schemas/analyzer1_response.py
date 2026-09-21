from pydantic import BaseModel

class Analyzer1Response(BaseModel):
    sample: str
    input_frequency_mhz: float
    delta_f_mhz: float
    mass_g: float
    delta_m_g_cm2: float
