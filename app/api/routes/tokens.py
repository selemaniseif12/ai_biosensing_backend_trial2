# app/routes/tokens.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.token_service import issue_token_for_service

router = APIRouter()

class TokenRequest(BaseModel):
    user_id: int
    service_name: str


@router.post("/tokens/issue")
async def issue_token(payload: TokenRequest):
    """
    Issues a token manually (admin or fallback).
    Normally tokens are issued automatically in payments.py.
    """

    token = issue_token_for_service(
        service_name=payload.service_name,
        user_id=payload.user_id
    )

    if not token:
        raise HTTPException(status_code=500, detail="Token issuance failed")

    return {"token": token}
