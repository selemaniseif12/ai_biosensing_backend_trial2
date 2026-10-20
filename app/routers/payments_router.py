import logging
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enrollment import Enrollment
from app.models.payment_receipt import PaymentReceipt


logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# STRIPE CONFIGURATION
# ---------------------------------------------------------

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not configured.")

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/payments", tags=["Payments"])


# ---------------------------------------------------------
# REQUEST MODELS
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
# STRIPE OBJECT CONVERSION
# ---------------------------------------------------------

def stripe_value_to_dict(value):
    """
    Recursively convert Stripe SDK objects into ordinary Python
    dictionaries and lists.

    This is important because the installed Stripe SDK returns
    resource objects that do not support dictionary-style .get().
    """

    if isinstance(value, dict):
        return {
            key: stripe_value_to_dict(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            stripe_value_to_dict(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            stripe_value_to_dict(item)
            for item in value
        ]

    converter = getattr(value, "to_dict", None)

    if callable(converter):
        return stripe_value_to_dict(converter())

    return value


# ---------------------------------------------------------
# MONEY HELPERS
# ---------------------------------------------------------

def positive_amount_to_cents(value) -> int:
    """Convert a positive monetary amount to integer cents."""

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid payment amount.",
        )

    if not amount.is_finite() or amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be positive and valid.",
        )

    cents = int(
        (amount * Decimal("100")).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )

    if cents < 1:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be at least one cent.",
        )

    return cents


# ---------------------------------------------------------
# RECEIPT HELPERS
# ---------------------------------------------------------

def generate_invoice_number(db: Session) -> str:
    """
    Generate a human-readable invoice number.

    Note: concurrent requests can still calculate the same number.
    The model's unique invoice_number constraint prevents both
    duplicate numbers from being stored, but one transaction may
    need to be retried if a collision occurs.
    """

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
        except (ValueError, AttributeError):
            last_seq = 0
    else:
        last_seq = 0

    return f"{prefix}{last_seq + 1:04d}"


def receipt_exists(
    db: Session,
    payment_intent_id: str,
) -> bool:
    """Check whether a receipt already exists for a PaymentIntent."""

    if not payment_intent_id:
        return False

    return (
        db.query(PaymentReceipt.id)
        .filter(
            PaymentReceipt.stripe_payment_intent_id
            == payment_intent_id
        )
        .first()
        is not None
    )


def create_payment_receipt(
    db: Session,
    *,
    user_id: int,
    service_name: str,
    amount_cents: int,
    currency: str,
    items: str,
    payment_intent_id: str,
) -> PaymentReceipt:
    """Create a receipt using verified Stripe payment information."""

    receipt = PaymentReceipt(
        user_id=user_id,
        invoice_number=generate_invoice_number(db),
        service_name=service_name,
        amount_paid=amount_cents / 100.0,
        currency=currency.lower(),
        items=items,
        stripe_payment_intent_id=payment_intent_id,
    )

    db.add(receipt)

    return receipt


# ---------------------------------------------------------
# CONSULTING PAYMENT — FIXED FEE
# ---------------------------------------------------------

@router.post("/consulting/fixed")
async def consulting_fixed(
    payload: ConsultingFixedRequest,
):
    if payload.user_id < 1:
        raise HTTPException(
            status_code=400,
            detail="A valid user ID is required.",
        )

    try:
        intent = stripe.PaymentIntent.create(
            amount=15000,
            currency="cad",
            metadata={
                "type": "consulting",
                "user_id": str(payload.user_id),
            },
        )

        return {
            "client_secret": intent.client_secret,
        }

    except HTTPException:
        raise

    except stripe.error.StripeError:
        logger.exception(
            "Unable to create fixed consulting PaymentIntent."
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to initiate consulting payment.",
        )

    except Exception:
        logger.exception(
            "Unexpected error creating fixed consulting PaymentIntent."
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while starting payment.",
        )


# ---------------------------------------------------------
# CONSULTING PAYMENT — CUSTOM FEE
# ---------------------------------------------------------

@router.post("/consulting/custom")
async def consulting_custom(
    payload: ConsultingCustomRequest,
):
    if payload.user_id < 1:
        raise HTTPException(
            status_code=400,
            detail="A valid user ID is required.",
        )

    amount_cents = positive_amount_to_cents(
        payload.consulting_fee
    )

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="cad",
            metadata={
                "type": "consulting",
                "user_id": str(payload.user_id),
            },
        )

        return {
            "client_secret": intent.client_secret,
        }

    except HTTPException:
        raise

    except stripe.error.StripeError:
        logger.exception(
            "Unable to create custom consulting PaymentIntent."
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to initiate consulting payment.",
        )

    except Exception:
        logger.exception(
            "Unexpected error creating custom consulting PaymentIntent."
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while starting payment.",
        )


# ---------------------------------------------------------
# COURSE PAYMENT
# ---------------------------------------------------------

@router.post("/course")
async def course_payment(
    payload: CoursePaymentRequest,
):
    if payload.user_id < 1 or payload.course_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Valid user and course IDs are required.",
        )

    amount_cents = positive_amount_to_cents(
        payload.price
    )

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="cad",
            metadata={
                "type": "course",
                "user_id": str(payload.user_id),
                "course_id": str(payload.course_id),
            },
        )

        return {
            "client_secret": intent.client_secret,
        }

    except HTTPException:
        raise

    except stripe.error.StripeError:
        logger.exception(
            "Unable to create course PaymentIntent."
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to initiate course payment.",
        )

    except Exception:
        logger.exception(
            "Unexpected error creating course PaymentIntent."
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while starting payment.",
        )


# ---------------------------------------------------------
# STRIPE WEBHOOK — VERIFIED PAYMENT PROCESSING
# ---------------------------------------------------------

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Process signed Stripe events.

    Store receipts are created only when Stripe reports a paid
    Checkout Session identified by metadata type='store'.

    Consulting and course PaymentIntents retain their existing
    receipt and enrollment workflow.
    """

    if not STRIPE_WEBHOOK_SECRET:
        logger.error(
            "STRIPE_WEBHOOK_SECRET is not configured."
        )

        raise HTTPException(
            status_code=500,
            detail="Stripe webhook is not configured.",
        )

    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe signature.",
        )

    # -----------------------------------------------------
    # VERIFY WEBHOOK SIGNATURE
    # -----------------------------------------------------

    try:
        stripe_event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET,
        )

        # IMPORTANT:
        # Convert the Event and all nested Stripe objects to
        # regular dictionaries before using dictionary methods.
        event = stripe_value_to_dict(stripe_event)

    except Exception:
        logger.warning(
            "Stripe webhook signature or payload verification failed."
        )

        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe webhook signature or payload.",
        )

    event_type = event["type"]
    event_object = event["data"]["object"]

    # -----------------------------------------------------
    # STORE CHECKOUT SESSION COMPLETED
    # -----------------------------------------------------

    if event_type in {
        "checkout.session.completed",
        "checkout.session.async_payment_succeeded",
    }:
        session = event_object

        # Never generate a paid receipt from an unpaid session.
        if (
            session.get("mode") != "payment"
            or session.get("payment_status") != "paid"
        ):
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ignored",
                    "reason": "checkout_not_paid",
                },
            )

        metadata = session.get("metadata") or {}

        # Ignore Checkout Sessions belonging to another service.
        if metadata.get("type") != "store":
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ignored",
                    "reason": "not_store_checkout",
                },
            )

        raw_user_id = (
            metadata.get("user_id")
            or session.get("client_reference_id")
        )

        try:
            user_id = int(raw_user_id)

            if user_id < 1:
                raise ValueError("User ID must be positive.")

        except (TypeError, ValueError):
            logger.error(
                "Paid store Checkout Session has invalid user metadata."
            )

            raise HTTPException(
                status_code=400,
                detail="Invalid user information in Checkout Session.",
            )

        session_id = session.get("id")
        payment_intent_id = session.get("payment_intent")
        amount_total = session.get("amount_total")
        currency = session.get("currency") or "usd"

        if (
            not session_id
            or not payment_intent_id
            or amount_total is None
        ):
            raise HTTPException(
                status_code=400,
                detail="Checkout Session is missing payment information.",
            )

        # Stripe can return a PaymentIntent ID or an expanded object.
        if isinstance(payment_intent_id, dict):
            payment_intent_id = payment_intent_id.get("id")

        if not isinstance(payment_intent_id, str):
            raise HTTPException(
                status_code=400,
                detail="Invalid PaymentIntent reference.",
            )

        if not payment_intent_id:
            raise HTTPException(
                status_code=400,
                detail="Empty PaymentIntent reference.",
            )

        # Idempotency check: avoid recording an existing payment twice.
        if receipt_exists(db, payment_intent_id):
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "duplicate": True,
                },
            )

        # -------------------------------------------------
        # RETRIEVE VERIFIED LINE ITEMS FROM STRIPE
        # -------------------------------------------------

        try:
            stripe_item_list = (
                stripe.checkout.Session.list_line_items(
                    session_id,
                    limit=100,
                )
            )

            # Stripe returns a resource object, not necessarily
            # a normal Python dictionary.
            stripe_items = stripe_value_to_dict(
                stripe_item_list
            )

            descriptions = []

            for item in stripe_items.get("data", []):
                name = item.get("description") or "Store item"
                quantity = item.get("quantity") or 1

                descriptions.append(
                    f"{name} x {quantity}"
                )

            items_description = "; ".join(descriptions)

            if not items_description:
                items_description = (
                    f"Store Checkout Session {session_id}"
                )

        except Exception:
            logger.exception(
                "Unable to retrieve Stripe Checkout line items."
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Unable to retrieve purchased items from Stripe."
                ),
            )

        # -------------------------------------------------
        # CREATE STORE PAYMENT RECEIPT
        # -------------------------------------------------

        try:
            receipt = create_payment_receipt(
                db,
                user_id=user_id,
                service_name="Store Purchase",
                amount_cents=int(amount_total),
                currency=currency,
                items=items_description,
                payment_intent_id=payment_intent_id,
            )

            db.commit()
            db.refresh(receipt)

        except Exception:
            db.rollback()

            logger.exception(
                "Failed to save receipt for verified store payment."
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Unable to record the verified store payment."
                ),
            )

        logger.info(
            "Store payment receipt created: invoice=%s user_id=%s",
            receipt.invoice_number,
            user_id,
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "invoice_number": receipt.invoice_number,
            },
        )

    # -----------------------------------------------------
    # CONSULTING AND COURSE PAYMENTINTENTS
    # -----------------------------------------------------

    if event_type == "payment_intent.succeeded":
        intent = event_object
        metadata = intent.get("metadata") or {}

        payment_type = metadata.get("type")

        # Store receipts are handled by Checkout Session events.
        if payment_type not in {
            "consulting",
            "course",
        }:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ignored",
                    "reason": "unsupported_payment_type",
                },
            )

        try:
            user_id = int(metadata.get("user_id"))

            if user_id < 1:
                raise ValueError("User ID must be positive.")

        except (TypeError, ValueError):
            logger.error(
                "Successful PaymentIntent has invalid user metadata."
            )

            raise HTTPException(
                status_code=400,
                detail="Invalid user information in PaymentIntent.",
            )

        payment_intent_id = intent.get("id")
        amount_cents = intent.get("amount_received")
        currency = intent.get("currency") or "cad"

        if (
            not payment_intent_id
            or amount_cents is None
        ):
            raise HTTPException(
                status_code=400,
                detail="PaymentIntent is missing payment information.",
            )

        if receipt_exists(db, payment_intent_id):
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "duplicate": True,
                },
            )

        # -------------------------------------------------
        # DETERMINE PAYMENT TYPE
        # -------------------------------------------------

        if payment_type == "consulting":
            service_name = "Consulting Payment"
            items_description = "Consulting Session"

        elif payment_type == "course":
            raw_course_id = metadata.get("course_id")

            try:
                course_id = int(raw_course_id)

                if course_id < 1:
                    raise ValueError("Course ID must be positive.")

            except (TypeError, ValueError):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Missing or invalid course ID in PaymentIntent."
                    ),
                )

            service_name = "Course Payment"
            items_description = f"Course ID: {course_id}"

        else:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ignored",
                },
            )

        # -------------------------------------------------
        # SAVE RECEIPT AND COURSE ENROLLMENT
        # -------------------------------------------------

        try:
            if payment_type == "course":
                existing_enrollment = (
                    db.query(Enrollment)
                    .filter(
                        Enrollment.user_id == user_id,
                        Enrollment.course_id == course_id,
                    )
                    .first()
                )

                if not existing_enrollment:
                    enrollment = Enrollment(
                        user_id=user_id,
                        course_id=course_id,
                        payment_status="paid",
                        enrollment_status="active",
                    )

                    db.add(enrollment)

            receipt = create_payment_receipt(
                db,
                user_id=user_id,
                service_name=service_name,
                amount_cents=int(amount_cents),
                currency=currency,
                items=items_description,
                payment_intent_id=payment_intent_id,
            )

            db.commit()
            db.refresh(receipt)

        except Exception:
            db.rollback()

            logger.exception(
                "Failed to record a verified consulting/course payment."
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to record the verified payment.",
            )

        logger.info(
            "Payment receipt created: invoice=%s user_id=%s type=%s",
            receipt.invoice_number,
            user_id,
            payment_type,
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "invoice_number": receipt.invoice_number,
            },
        )

    # -----------------------------------------------------
    # ACKNOWLEDGE UNRELATED STRIPE EVENTS
    # -----------------------------------------------------

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "event": event_type,
        },
    )