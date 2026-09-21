import stripe
from fastapi import APIRouter, Request
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.receipt import Receipt
import json

router = APIRouter(tags=["Stripe"])

endpoint_secret = "YOUR_WEBHOOK_SECRET"

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return {"error": "Invalid signature"}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])

        # Create receipt
        receipt = Receipt(
            user_id=user_id,
            total_usd=session["amount_total"] / 100,
            items_json=json.dumps(session["line_items"]),
        )

        db.add(receipt)
        db.commit()

    return {"status": "success"}
