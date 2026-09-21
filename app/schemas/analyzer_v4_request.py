from pydantic import BaseModel
from typing import List

class AnalyzerV4Request(BaseModel):
    sensor_data: List[float]
