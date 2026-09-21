from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/dashboard/ml", tags=["ML Advanced"])

# ---------------------------
# Drift Detection
# ---------------------------
class DriftResponse(BaseModel):
    timestamps: List[str]
    values: List[float]

@router.get("/drift", response_model=DriftResponse)
def get_drift_data():
    return DriftResponse(
        timestamps=["10:00","10:05","10:10","10:15","10:20"],
        values=[0.02, 0.05, 0.04, 0.07, 0.10]
    )

# ---------------------------
# ROC Curve
# ---------------------------
class RocResponse(BaseModel):
    fpr: List[float]
    tpr: List[float]

@router.get("/roc", response_model=RocResponse)
def get_roc_curve():
    return RocResponse(
        fpr=[0.0, 0.1, 0.2, 0.3, 1.0],
        tpr=[0.0, 0.4, 0.7, 0.9, 1.0]
    )

# ---------------------------
# Confusion Matrix
# ---------------------------
class ConfusionResponse(BaseModel):
    matrix: List[List[int]]

@router.get("/confusion", response_model=ConfusionResponse)
def get_confusion_matrix():
    return ConfusionResponse(
        matrix=[
            [50, 5],
            [3, 42]
        ]
    )
