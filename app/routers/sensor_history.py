from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random
import datetime

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage

router = APIRouter(prefix="/sensor", tags=["Sensor"])

class SensorPoint(BaseModel):
    timestamp: str
    value: float


@router.get("/history", response_model=List[SensorPoint])
def get_sensor_history(token: str):
    """
    Returns 30 historical sensor points.
    - Rate-limited
    - Usage logged
    """

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="sensor_history")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="sensor_history",
        details="Requested 30 historical sensor points"
    )

    # ORIGINAL LOGIC (unchanged)
    now = datetime.datetime.utcnow()
    data = []

    for i in range(30):
        ts = (now - datetime.timedelta(seconds=5 * i)).isoformat()
        data.append(SensorPoint(timestamp=ts, value=random.uniform(0.1, 1.0)))

    return list(reversed(data))
