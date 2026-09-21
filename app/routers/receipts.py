# app/routes/receipts.py

from fastapi import APIRouter, HTTPException
from app.services.receipt_service import (
    get_receipts_for_user,
    get_receipt_by_id,
    create_receipt
)
from pydantic import BaseModel

router = APIRouter()

class ReceiptCreate(BaseModel):
    user_id: int
    service_name: str
    amount_paid: float
    transaction_id: str
    token_issued: str
    items_json: str | None = None


@router.get("/receipts/list")
async def list_receipts(user_id: int):
    """
    Returns all receipts for a given user.
    """
    receipts = get_receipts_for_user(user_id)
    return {"receipts": receipts}


@router.get("/receipts/{receipt_id}")
async def get_receipt(receipt_id: int):
    """
    Returns a single receipt by ID.
    """
    receipt = get_receipt_by_id(receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.post("/receipts/create")
async def create_new_receipt(payload: ReceiptCreate):
    """
    Optional manual receipt creation endpoint.
    Normally receipts are created automatically in payments.py.
    """
    receipt = create_receipt(
        user_id=payload.user_id,
        service_name=payload.service_name,
        amount_paid=payload.amount_paid,
        transaction_id=payload.transaction_id,
        token=payload.token_issued,
        date=None  # service will auto‑assign datetime.utcnow()
    )

    return {"created": True, "receipt": receipt}
