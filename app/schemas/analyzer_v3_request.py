from pydantic import BaseModel
from typing import List

class AnalyzerV3Request(BaseModel):
    sensor_data: List[float]
