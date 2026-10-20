import logging
import os
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.cart_item import CartItem
from app.models.products import Product
from app.models.user import User


logger = logging.getLogger(__name__)

router = APIRouter(tags=["Stripe"])


# ---------------------------------------------------------
# STRIPE CONFIGURATION
# ---------------------------------------------------------

STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")

FRONTEND_BASE_URL = os.getenv(
    "FRONTEND_BASE_URL",
    "https://ai-biosensing-frontend-v2.vercel.app",
).rstrip("/")


if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET
    stripe_enabled = True
else:
    stripe_enabled = False
    logger.warning(
        "STRIPE_SECRET_KEY is not configured. "
        "Stripe checkout is disabled."
    )


# ---------------------------------------------------------
# CREATE STRIPE CHECKOUT SESSION
# ---------------------------------------------------------

@router.post("/stripe/checkout")
def stripe_checkout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a Stripe-hosted Checkout Session for the authenticated
    customer's cart.

    The customer ID comes from the verified JWT, not from a
    query parameter supplied by the browser.

    Current product prices are retrieved from the product catalogue
    so cached cart prices are not used as the authoritative amount.
    """

    if not stripe_enabled:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured on this server.",
        )

    user_id = current_user.id

    if not user_id or user_id < 1:
        raise HTTPException(
            status_code=401,
            detail="A valid authenticated customer is required.",
        )

    # -----------------------------------------------------
    # LOAD AUTHENTICATED CUSTOMER'S CART
    # -----------------------------------------------------

    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty.",
        )

    # -----------------------------------------------------
    # PREPARE STRIPE LINE ITEMS USING CATALOGUE PRICES
    # -----------------------------------------------------

    line_items = []

    for item in cart_items:
        # Retrieve the authoritative product record.
        product = (
            db.query(Product)
            .filter(Product.item_id == item.item_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Product '{item.item_id}' is no longer available. "
                    "Please update your cart."
                ),
            )

        try:
            price = Decimal(str(product.price_usd))
            quantity = int(item.quantity)
        except (InvalidOperation, TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="The cart contains an invalid price or quantity.",
            )

        if not price.is_finite() or price <= 0:
            raise HTTPException(
                status_code=400,
                detail="Product prices must be positive and valid.",
            )

        if quantity < 1:
            raise HTTPException(
                status_code=400,
                detail="Cart item quantities must be positive integers.",
            )

        # Stripe requires integer cents for USD line-item prices.
        unit_amount = int(
            (price * Decimal("100")).quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )

        if unit_amount < 1:
            raise HTTPException(
                status_code=400,
                detail="The product price must be at least one cent.",
            )

        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name or "Store item",
                    },
                    "unit_amount": unit_amount,
                },
                "quantity": quantity,
            }
        )

    if not line_items:
        raise HTTPException(
            status_code=400,
            detail="No valid items were found in the cart.",
        )

    # -----------------------------------------------------
    # CREATE STRIPE CHECKOUT SESSION
    # -----------------------------------------------------

    try:
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",

            success_url=(
                f"{FRONTEND_BASE_URL}/dashboard?payment=success"
            ),
            cancel_url=(
                f"{FRONTEND_BASE_URL}/dashboard?payment=cancel"
            ),

            metadata={
                "user_id": str(user_id),
                "type": "store",
            },

            client_reference_id=str(user_id),

            payment_intent_data={
                "metadata": {
                    "user_id": str(user_id),
                    "type": "store",
                }
            },
        )

        if not session.url:
            logger.error(
                "Stripe returned a Checkout Session without a URL."
            )

            raise HTTPException(
                status_code=502,
                detail="Stripe did not return a checkout URL.",
            )

        logger.info(
            "Stripe Checkout Session created for authenticated user_id=%s",
            user_id,
        )

        return {
            "checkout_url": session.url,
            "session_id": session.id,
        }

    except HTTPException:
        raise

    except stripe.error.StripeError:
        logger.exception(
            "Stripe failed to create a Checkout Session."
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to start Stripe checkout. Please try again.",
        )

    except Exception:
        logger.exception(
            "Unexpected error while creating Stripe checkout."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while starting checkout."
            ),
        )