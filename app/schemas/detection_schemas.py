from pydantic import BaseModel

class DetectionRequest(BaseModel):
    virus_id: int
    device_id: int
    delta_f_mhz: float
    frequency_mhz: float
    deposition_rate: float
    temperature: float
    humidity: float
    flow_rate: float

class DetectionResponse(BaseModel):
    virus: str
    device_id: int
    physics_estimated_count: float
    physics_mass_change_fg: float
    ml_estimated_time_to_detection: float
    ml_confidence: float
