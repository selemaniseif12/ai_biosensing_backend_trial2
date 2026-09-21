# app/routes/payments.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.services.token_service import issue_token_for_service
from app.services.receipt_service import create_receipt

router = APIRouter()

class PaymentSuccess(BaseModel):
    user_id: int
    service_name: str
    amount_paid: float
    transaction_id: str

@router.post("/payments/success")
async def payment_success(payload: PaymentSuccess):
    """
    Called after Stripe payment success.
    1. Issues token for purchased service.
    2. Creates receipt.
    3. Returns both to frontend.
    """

    # 1. Issue token automatically
    token = issue_token_for_service(
        service_name=payload.service_name,
        user_id=payload.user_id
    )

    if not token:
        raise HTTPException(status_code=500, detail="Token issuance failed")

    # 2. Create receipt
    receipt = create_receipt(
        user_id=payload.user_id,
        service_name=payload.service_name,
        amount_paid=payload.amount_paid,
        transaction_id=payload.transaction_id,
        token=token,
        date=datetime.utcnow()
    )

    # 3. Return receipt + token to frontend
    return {
        "success": True,
        "service": payload.service_name,
        "token": token,
        "receipt": receipt
    }
