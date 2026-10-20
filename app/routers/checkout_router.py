from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
)


@router.post("")
def process_checkout():
    """
    Legacy checkout endpoint.

    This endpoint previously reported a successful payment without
    collecting or verifying payment.

    Customers must now use the Stripe Checkout endpoint instead.
    This endpoint intentionally does not mark orders as paid,
    issue receipts, or modify cart contents.
    """

    raise HTTPException(
        status_code=410,
        detail={
            "message": (
                "This legacy checkout endpoint is disabled. "
                "Start payment through the Stripe Checkout endpoint."
            ),
            "payment_endpoint": (
                "/store/stripe/checkout?user_id=<authenticated_user_id>"
            ),
            "payment_status": "not_processed",
        },
    )