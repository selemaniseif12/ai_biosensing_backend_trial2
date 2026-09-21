from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models.subscription import Subscription
from app.auth.auth import get_current_user


# -----------------------------
# Subscription Router (FIXED)
# -----------------------------
router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"],
    dependencies=[Depends(get_current_user)]   # ⭐ FIX: Swagger now sends the token
)


# -----------------------------
# Request Model for Activation
# -----------------------------
class SubscriptionActivateRequest(BaseModel):
    plan_name: str
    duration_days: int
    payment_reference: str


@router.post("/activate")
def activate_subscription(
    data: SubscriptionActivateRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow() + timedelta(days=data.duration_days)

    sub = Subscription(
        user_id=user.id,
        plan_name=data.plan_name,
        start_date=datetime.utcnow(),
        end_date=end_date,
        status="active",
        payment_reference=data.payment_reference
    )

    db.add(sub)
    db.commit()
    db.refresh(sub)

    return {
        "message": "Subscription activated",
        "plan": data.plan_name,
        "expires": end_date
    }


# -----------------------------
# Request Model for Renewal
# -----------------------------
class SubscriptionRenewRequest(BaseModel):
    duration_days: int


@router.post("/renew")
def renew_subscription(
    data: SubscriptionRenewRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .order_by(Subscription.end_date.desc())
        .first()
    )

    if not sub:
        raise HTTPException(status_code=404, detail="No subscription found")

    sub.end_date = sub.end_date + timedelta(days=data.duration_days)
    sub.status = "active"

    db.commit()
    db.refresh(sub)

    return {
        "message": "Subscription renewed",
        "new_expiry": sub.end_date
    }


@router.get("/status")
def subscription_status(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .order_by(Subscription.end_date.desc())
        .first()
    )

    if not sub:
        return {"active": False, "reason": "No subscription found"}

    if sub.end_date < datetime.utcnow():
        sub.status = "expired"
        db.commit()

    return {
        "active": sub.status == "active",
        "plan": sub.plan_name,
        "expires": sub.end_date,
        "status": sub.status
    }


@router.get("/verify-access")
def verify_access(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .order_by(Subscription.end_date.desc())
        .first()
    )

    if not sub or sub.end_date < datetime.utcnow():
        raise HTTPException(
            status_code=403,
            detail="Subscription expired or missing. Please renew."
        )

    return {"access": True, "plan": sub.plan_name}
