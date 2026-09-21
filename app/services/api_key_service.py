import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# ⭐ FIXED — correct model import
from app.models.customer import Customer


class APIKeyObject:
    def __init__(self, key: str):
        self.key = key


def generate_api_key() -> str:
    """Generate a secure random API key."""
    return secrets.token_hex(32)


def create_api_key_for_customer(db: Session, customer: Customer) -> APIKeyObject:
    """Generate and assign a new API key to a customer."""
    api_key_value = generate_api_key()
    customer.api_key = api_key_value
    db.commit()
    db.refresh(customer)
    return APIKeyObject(api_key_value)


def validate_api_key(db: Session, api_key: str) -> Customer:
    """
    Validate API key AND enforce:
    - customer exists
    - customer is active
    - customer is within monthly usage limit
    """
    customer = db.query(Customer).filter(Customer.api_key == api_key).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    if not customer.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer account is inactive"
        )

    if customer.monthly_usage >= customer.monthly_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Monthly API usage limit exceeded"
        )

    # Increment usage
    customer.monthly_usage += 1
    db.commit()

    return customer


# ============================================================
# ⭐ NEW — FUNCTION REQUIRED BY auth.py
# ============================================================

def validate_api_key_in_db(db: Session, api_key: str) -> bool:
    """
    Lightweight validator used by /auth/validate-key.
    Returns True/False instead of raising exceptions.
    """
    customer = db.query(Customer).filter(Customer.api_key == api_key).first()
    return customer is not None
