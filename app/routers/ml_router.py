from fastapi import APIRouter
from app.ml.classifier import MLInput, classify

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

@router.post("/classify")
def classify_endpoint(payload: MLInput):
    return classify(payload)
