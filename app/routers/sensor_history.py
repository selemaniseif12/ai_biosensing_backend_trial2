from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random
import datetime

router = APIRouter(prefix="/sensor", tags=["Sensor"])

class SensorPoint(BaseModel):
    timestamp: str
    value: float

@router.get("/history", response_model=List[SensorPoint])
def get_sensor_history():
    now = datetime.datetime.utcnow()
    data = []

    for i in range(30):
        ts = (now - datetime.timedelta(seconds=5*i)).isoformat()
        data.append(SensorPoint(timestamp=ts, value=random.uniform(0.1, 1.0)))

    return list(reversed(data))
