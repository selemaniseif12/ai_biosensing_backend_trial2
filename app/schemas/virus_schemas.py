from pydantic import BaseModel

class VirusBase(BaseModel):
    id: int
    name: str
    antibody: str
    antigen: str
    mass_fg: float
    default_device_id: int
    virus_counts_per_device: float

    class Config:
        orm_mode = True
