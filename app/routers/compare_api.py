from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.token_verifier import verify_token
from app.schemas.compare import CompareRequest
from app.services.compare_service import run_compare_analysis
from app.services.usage_service import service_create_usage_log

router = APIRouter(
    prefix="/compare",
    tags=["Compare API"]
)

# ---------------------------------------------------------
# Compare API (requires token)
# ---------------------------------------------------------
@router.post("/")
def compare_endpoint(
    payload: CompareRequest,
    token: str,
    db: Session = Depends(get_db)
):
    # Verify token for compare service
    verify_token(token, "compare_v2", db)

    # Run compare analysis model
    result = run_compare_analysis(payload)

    # Log usage
    service_create_usage_log(
        db,
        {
            "service_name": "compare_v2",
            "token": token,
            "input_data": payload.dict(),
            "output_data": result
        }
    )

    return {"success": True, "result": result}
