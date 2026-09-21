from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.token_verifier import verify_token
from app.schemas.ml import MLRequest
from app.services.ml_service import run_ml_v2, run_ml_v6
from app.services.usage_service import service_create_usage_log

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning API"]
)

# ---------------------------------------------------------
# ML v2 (requires token)
# ---------------------------------------------------------
@router.post("/v2")
def ml_v2_endpoint(
    payload: MLRequest,
    token: str,
    db: Session = Depends(get_db)
):
    # Verify token for ML v2
    verify_token(token, "ml_v2", db)

    # Run ML model
    result = run_ml_v2(payload)

    # Log usage
    service_create_usage_log(
        db,
        {
            "service_name": "ml_v2",
            "token": token,
            "input_data": payload.dict(),
            "output_data": result
        }
    )

    return {"success": True, "result": result}


# ---------------------------------------------------------
# ML v6 (requires token)
# ---------------------------------------------------------
@router.post("/v6")
def ml_v6_endpoint(
    payload: MLRequest,
    token: str,
    db: Session = Depends(get_db)
):
    # Verify token for ML v6
    verify_token(token, "ml_v6", db)

    # Run ML model
    result = run_ml_v6(payload)

    # Log usage
    service_create_usage_log(
        db,
        {
            "service_name": "ml_v6",
            "token": token,
            "input_data": payload.dict(),
            "output_data": result
        }
    )

    return {"success": True, "result": result}
