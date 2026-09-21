# app/services/receipt_service.py

from datetime import datetime
from app.models.receipt import Receipt
from app.database import db_session

def create_receipt(user_id: int, service_name: str, amount_paid: float,
                   transaction_id: str, token: str, date: datetime):
    """
    Creates a receipt entry in the database after successful payment.
    """

    receipt = Receipt(
        user_id=user_id,
        service_name=service_name,
        amount_paid=amount_paid,
        transaction_id=transaction_id,
        token_issued=token,
        date=date
    )

    db_session.add(receipt)
    db_session.commit()
    db_session.refresh(receipt)

    return {
        "receipt_id": receipt.id,
        "user_id": receipt.user_id,
        "service_name": receipt.service_name,
        "amount_paid": receipt.amount_paid,
        "transaction_id": receipt.transaction_id,
        "token_issued": receipt.token_issued,
        "date": receipt.date.isoformat()
    }


def get_receipts_for_user(user_id: int):
    """
    Returns all receipts for a given user.
    """

    receipts = db_session.query(Receipt).filter(
        Receipt.user_id == user_id
    ).order_by(Receipt.date.desc()).all()

    return [
        {
            "receipt_id": r.id,
            "service_name": r.service_name,
            "amount_paid": r.amount_paid,
            "transaction_id": r.transaction_id,
            "token_issued": r.token_issued,
            "date": r.date.isoformat()
        }
        for r in receipts
    ]


def get_receipt_by_id(receipt_id: int):
    """
    Returns a single receipt by ID.
    """

    receipt = db_session.query(Receipt).filter(
        Receipt.id == receipt_id
    ).first()

    if not receipt:
        return None

    return {
        "receipt_id": receipt.id,
        "user_id": receipt.user_id,
        "service_name": receipt.service_name,
        "amount_paid": receipt.amount_paid,
        "transaction_id": receipt.transaction_id,
        "token_issued": receipt.token_issued,
        "date": receipt.date.isoformat()
    }
