from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

class PredictionInput(BaseModel):
    frequency_mhz: float
    delta_f_mhz: float
    device_thickness_mm: float

@router.post("/predict")
def predict(data: PredictionInput):
    # Simple mock model
    score = (
        data.frequency_mhz * 0.1 +
        data.delta_f_mhz * 2.5 +
        data.device_thickness_mm * 0.8
    )

    return {
        "prediction_score": score,
        "risk_level": (
            "High" if score > 50 else
            "Medium" if score > 20 else
            "Low"
        )
    }
