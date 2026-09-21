from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.token_model import ServiceToken

router = APIRouter(prefix="/tokens", tags=["Service Tokens"])

class TokenIssueRequest(BaseModel):
    service_name: str
    user_id: int | None = None

class TokenValidateRequest(BaseModel):
    token: str
    service_name: str

class TokenRevokeRequest(BaseModel):
    token: str

@router.post("/issue")
async def issue_token(payload: TokenIssueRequest, db: Session = Depends(get_db)):
    token_record = ServiceToken.create_token(
        db=db,
        service_name=payload.service_name,
        user_id=payload.user_id
    )
    return {"token": token_record.token}

@router.post("/validate")
async def validate_token(payload: TokenValidateRequest, db: Session = Depends(get_db)):
    token = (
        db.query(ServiceToken)
        .filter(
            ServiceToken.token == payload.token,
            ServiceToken.service_name == payload.service_name,
            ServiceToken.is_active == True
        )
        .first()
    )
    if not token:
        raise HTTPException(status_code=403, detail="Invalid or inactive token")
    return {"valid": True}

@router.post("/revoke")
async def revoke_token(payload: TokenRevokeRequest, db: Session = Depends(get_db)):
    token = (
        db.query(ServiceToken)
        .filter(ServiceToken.token == payload.token)
        .first()
    )
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.is_active = False
    db.commit()
    return {"revoked": True}
