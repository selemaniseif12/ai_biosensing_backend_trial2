# app/utils/payment_verification.py

import stripe
import os

# Load Stripe secret key from environment
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not set")

stripe.api_key = STRIPE_SECRET_KEY


def verify_payment(payment_intent_id: str) -> bool:
    """
    Verifies whether a Stripe PaymentIntent has succeeded.
    Used by payments.py to grant service access tokens.
    """

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Only allow access if payment succeeded
        return intent.status == "succeeded"

    except Exception:
        return False