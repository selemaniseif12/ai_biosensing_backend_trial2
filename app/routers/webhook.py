from fastapi import APIRouter, Request, HTTPException, Depends
import stripe
from sqlalchemy.orm import Session

# Correct imports for your project
from app.database import get_db
from app.models.students import Student as User
from app.models.subscription import Subscription

from datetime import datetime, timedelta

router = APIRouter(tags=["Stripe Webhook"])

# ⭐ Your real Stripe webhook secret
WEBHOOK_SECRET = "whsec_ba08549a9ad94327ef75e04d2738a080e6ec274150e3726bfbc053b08c631415"


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        item_id = session["metadata"].get("item_id")
        plan_name = session["metadata"].get("plan_name")
        duration_days = int(session["metadata"].get("duration_days", 30))

        customer_email = session.get("customer_details", {}).get("email")

        user = db.query(User).filter(User.email == customer_email).first()
        if not user:
            return {"status": "no-user"}

        end_date = datetime.utcnow() + timedelta(days=duration_days)

        subscription = Subscription(
            user_id=user.id,
            plan_name=plan_name,
            start_date=datetime.utcnow(),
            end_date=end_date,
            status="active",
            payment_reference=session["id"]
        )

        db.add(subscription)
        db.commit()

    return {"status": "success"}
