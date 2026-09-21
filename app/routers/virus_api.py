from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.token_verifier import verify_token
from app.schemas.virus import VirusRequest
from app.services.virus_service import run_virus_analysis
from app.services.usage_service import service_create_usage_log

router = APIRouter(
    prefix="/virus",
    tags=["Virus Analysis API"]
)

# ---------------------------------------------------------
# Virus List / Virus Analysis (requires token)
# ---------------------------------------------------------
@router.post("/analyze")
def virus_analysis_endpoint(
    payload: VirusRequest,
    token: str,
    db: Session = Depends(get_db)
):
    # Verify token for virus list service
    verify_token(token, "virus_list", db)

    # Run virus analysis model
    result = run_virus_analysis(payload)

    # Log usage
    service_create_usage_log(
        db,
        {
            "service_name": "virus_list",
            "token": token,
            "input_data": payload.dict(),
            "output_data": result
        }
    )

    return {"success": True, "result": result}
