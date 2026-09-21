# app/services/payment_service.py

from datetime import datetime
from app.services.token_service import issue_token_for_service
from app.services.receipt_service import create_receipt

def process_successful_payment(user_id: int, service_name: str,
                               amount_paid: float, transaction_id: str):
    """
    Handles full payment workflow:
    1. Issue token
    2. Create receipt
    3. Return both
    """

    # Issue token for purchased service
    token = issue_token_for_service(
        service_name=service_name,
        user_id=user_id
    )

    # Create receipt
    receipt = create_receipt(
        user_id=user_id,
        service_name=service_name,
        amount_paid=amount_paid,
        transaction_id=transaction_id,
        token=token,
        date=datetime.utcnow()
    )

    return {
        "token": token,
        "receipt": receipt
    }
