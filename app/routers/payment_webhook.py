from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.token_model import TokenModel   # ⭐ FIXED IMPORT

from app.services.email_service import send_email

router = APIRouter(prefix="/payment", tags=["Payment Webhook"])

@router.post("/webhook")
def payment_webhook(payload: dict, db: Session = Depends(get_db)):
    if payload.get("status") != "paid":
        raise HTTPException(400, "Payment not confirmed")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(404, "User not found")

    # ⭐ FIXED: Use TokenModel instead of ServiceToken
    token = TokenModel.create_token(
        db,
        token_type=payload["service_name"],
        user_id=user.id,
        description=f"Access token for {payload['service_name']}"
    )

    send_email(user.email, "Your Access Token", f"Your token: {token.token}")

    return {"status": "success", "token": token.token}
