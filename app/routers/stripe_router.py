import stripe
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart_item import CartItem
import os

router = APIRouter(tags=["Stripe"])

# ---------------------------------------------------------
# SAFE STRIPE INITIALIZATION
# ---------------------------------------------------------
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")

if not STRIPE_SECRET:
    # Stripe disabled, but router still loads safely
    print("⚠️ WARNING: STRIPE_SECRET_KEY is missing. Stripe checkout is disabled.")
    stripe_enabled = False
else:
    stripe.api_key = STRIPE_SECRET
    stripe_enabled = True


# ---------------------------------------------------------
# Create Stripe Checkout Session (SAFE)
# ---------------------------------------------------------
@router.post("/stripe/checkout")
def stripe_checkout(user_id: int, db: Session = Depends(get_db)):
    # If Stripe is disabled, return clean error
    if not stripe_enabled:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured on this server."
        )

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Build Stripe line items
    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.item_name
                },
                "unit_amount": int(item.price_usd * 100)
            },
            "quantity": item.quantity
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="https://piezo-sensors.com/dashboard/admin/checkout?success=true",
            cancel_url="https://piezo-sensors.com/dashboard/admin/checkout?canceled=true",
            metadata={"user_id": user_id}
        )

        return {"checkout_url": session.url}

    except Exception as e:
        # Stripe errors no longer break router loading
        raise HTTPException(
            status_code=500,
            detail=f"Stripe error: {str(e)}"
        )
