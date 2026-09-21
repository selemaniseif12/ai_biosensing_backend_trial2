import os
import stripe
import traceback
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.enrollment import Enrollment
from app.models.payment_receipt import PaymentReceipt

# ---------------------------------------------------------
# Stripe configuration
# ---------------------------------------------------------
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not set in environment.")

stripe.api_key = STRIPE_SECRET_KEY
print("Stripe key loaded:", stripe.api_key)

router = APIRouter(prefix="/payments", tags=["Payments"])

# ---------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------
class ConsultingFixedRequest(BaseModel):
    user_id: int

class ConsultingCustomRequest(BaseModel):
    user_id: int
    consulting_fee: float

class CoursePaymentRequest(BaseModel):
    user_id: int
    course_id: int
    price: float

# ---------------------------------------------------------
# Invoice Number Generator
# ---------------------------------------------------------
def generate_invoice_number(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"INV-{year}-"

    last = (
        db.query(PaymentReceipt)
        .filter(PaymentReceipt.invoice_number.like(f"{prefix}%"))
        .order_by(PaymentReceipt.invoice_number.desc())
        .first()
    )

    if last:
        try:
            last_seq = int(last.invoice_number.split("-")[-1])
        except:
            last_seq = 0
    else:
        last_seq = 0

    new_seq = last_seq + 1
    return f"{prefix}{new_seq:04d}"

# ---------------------------------------------------------
# Consulting Payment — Fixed $150 CAD
# ---------------------------------------------------------
@router.post("/consulting/fixed")
async def consulting_fixed(payload: ConsultingFixedRequest):
    try:
        FIXED_AMOUNT_CENTS = 15000  # $150 CAD

        intent = stripe.PaymentIntent.create(
            amount=FIXED_AMOUNT_CENTS,
            currency="cad",
            metadata={
                "type": "consulting",
                "user_id": payload.user_id,
            }
        )

        return {"client_secret": intent.client_secret}

    except Exception as e:
        print("STRIPE ERROR (fixed consulting):", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")

# ---------------------------------------------------------
# Consulting Payment — Custom Fee
# ---------------------------------------------------------
@router.post("/consulting/custom")
async def consulting_custom(payload: ConsultingCustomRequest):
    try:
        if payload.consulting_fee <= 0:
            raise HTTPException(status_code=400, detail="consulting_fee must be > 0")

        amount_cents = int(payload.consulting_fee * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="cad",
            metadata={
                "type": "consulting",
                "user_id": payload.user_id,
            }
        )

        return {"client_secret": intent.client_secret}

    except Exception as e:
        print("STRIPE ERROR (custom consulting):", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")

# ---------------------------------------------------------
# Course Payment
# ---------------------------------------------------------
@router.post("/course")
async def course_payment(payload: CoursePaymentRequest):
    try:
        if payload.price <= 0:
            raise HTTPException(status_code=400, detail="price must be > 0")

        amount_cents = int(payload.price * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="cad",
            metadata={
                "type": "course",
                "user_id": payload.user_id,
                "course_id": payload.course_id,
            }
        )

        return {"client_secret": intent.client_secret}

    except Exception as e:
        print("STRIPE ERROR (course payment):", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")

# ---------------------------------------------------------
# Webhook — Auto‑Generate Receipts
# ---------------------------------------------------------
@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured.")

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        print("WEBHOOK SIGNATURE ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        metadata = intent.get("metadata", {})

        payment_type = metadata.get("type")
        user_id = int(metadata.get("user_id")) if metadata.get("user_id") else None

        amount_cents = intent.get("amount", 0)
        amount_paid = amount_cents / 100.0
        currency = intent.get("currency", "cad")
        stripe_payment_intent_id = intent.get("id")

        service_name = None
        items_desc = ""

        # Consulting Payment
        if payment_type == "consulting":
            service_name = "Consulting Payment"
            items_desc = "Consulting Session"

        # Course Payment
        if payment_type == "course":
            course_id_raw = metadata.get("course_id")
            if course_id_raw is None:
                raise HTTPException(status_code=400, detail="Missing course_id in metadata.")

            course_id = int(course_id_raw)
            service_name = "Course Payment"
            items_desc = f"Course ID: {course_id}"

            existing = (
                db.query(Enrollment)
                .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
                .first()
            )

            if not existing:
                enrollment = Enrollment(
                    user_id=user_id,
                    course_id=course_id,
                    payment_status="paid",
                    enrollment_status="active",
                )
                db.add(enrollment)
                db.commit()

        # Create Receipt
        if user_id and service_name:
            invoice_number = generate_invoice_number(db)

            receipt = PaymentReceipt(
                user_id=user_id,
                invoice_number=invoice_number,
                service_name=service_name,
                amount_paid=amount_paid,
                currency=currency,
                items=items_desc,
                stripe_payment_intent_id=stripe_payment_intent_id,
            )

            db.add(receipt)
            db.commit()

            print(f"Receipt created: {invoice_number} for user {user_id}")

    return JSONResponse(status_code=200, content={"status": "success"})
