from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.ml.ml_integration import predict

router = APIRouter()

class PredictRequest(BaseModel):
    features: List[float]

@router.post("/ml/predict")
def ml_predict(payload: PredictRequest):
    try:
        result = predict(payload.features)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
