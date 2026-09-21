# payments.py

import os
import stripe
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import STRIPE_PRICE_IDS
from app.utils.payment_verification import verify_payment
from app.utils.token_generator import generate_token
from app.database import get_db
from app.models.token_model import TokenModel   # ⭐ FIXED IMPORT

router = APIRouter(prefix="/payments", tags=["Checkout + Access"])

# Load Stripe key from environment
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not set")
stripe.api_key = STRIPE_SECRET_KEY

# ---------------------------------------------------------
# 1. Create Checkout Session
# ---------------------------------------------------------
@router.post("/create-checkout-session")
async def create_checkout_session(item_id: str):
    if item_id not in STRIPE_PRICE_IDS:
        raise HTTPException(status_code=400, detail="Invalid item_id")

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{"price": STRIPE_PRICE_IDS[item_id], "quantity": 1}],
            metadata={"item_id": item_id},
            success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/cancel"
        )
        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 2. Grant service access tokens after payment
# ---------------------------------------------------------
class AccessRequest(BaseModel):
    payment_id: str
    item_id: str
    user_id: int | None = None

@router.post("/grant-access")
async def grant_access(payload: AccessRequest, db: Session = Depends(get_db)):
    # Verify payment
    if not verify_payment(payload.payment_id):
        raise HTTPException(status_code=400, detail="Payment verification failed")

    # Generate token
    token_value = generate_token()

    # ⭐ FIXED: Use TokenModel instead of ServiceToken
    token_record = TokenModel(
        token=token_value,
        token_type=payload.item_id,
        user_id=payload.user_id,
        description=f"Access token for {payload.item_id}",
        is_active=True,
    )

    db.add(token_record)
    db.commit()
    db.refresh(token_record)

    return {"success": True, "token": token_value}
