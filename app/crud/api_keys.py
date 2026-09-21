from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.api_key import APIKey


# ---------------------------------------------------------
# Create API Key
# ---------------------------------------------------------
def create_api_key(
    db: Session,
    customer_id: int,
    name: Optional[str] = None,
    monthly_limit: int = 0
) -> APIKey:
    key_value = APIKey.generate_key()

    api_key = APIKey(
        key=key_value,
        customer_id=customer_id,
        name=name,
        monthly_limit=monthly_limit,
        active=True,
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key


# ---------------------------------------------------------
# Get API Key by value
# ---------------------------------------------------------
def get_api_key_by_value(db: Session, key_value: str) -> Optional[APIKey]:
    return db.query(APIKey).filter(APIKey.key == key_value).first()


# ---------------------------------------------------------
# List all API keys for a customer
# ---------------------------------------------------------
def list_api_keys_for_customer(db: Session, customer_id: int) -> List[APIKey]:
    return (
        db.query(APIKey)
        .filter(APIKey.customer_id == customer_id)
        .order_by(APIKey.created_at.desc())
        .all()
    )


# ---------------------------------------------------------
# Revoke API Key
# ---------------------------------------------------------
def revoke_api_key(db: Session, api_key: APIKey) -> APIKey:
    api_key.active = False
    api_key.revoked_at = datetime.utcnow()

    db.commit()
    db.refresh(api_key)

    return api_key


# ---------------------------------------------------------
# Activate API Key
# ---------------------------------------------------------
def activate_api_key(db: Session, api_key: APIKey) -> APIKey:
    api_key.active = True
    api_key.revoked_at = None

    db.commit()
    db.refresh(api_key)

    return api_key


# ---------------------------------------------------------
# Rotate API Key (generate new key)
# ---------------------------------------------------------
def rotate_api_key(db: Session, api_key: APIKey) -> APIKey:
    api_key.key = APIKey.generate_key()
    api_key.created_at = datetime.utcnow()
    api_key.revoked_at = None
    api_key.active = True

    db.commit()
    db.refresh(api_key)

    return api_key


# ---------------------------------------------------------
# Increment usage count
# ---------------------------------------------------------
def increment_usage(db: Session, api_key: APIKey) -> APIKey:
    api_key.total_calls += 1

    db.commit()
    db.refresh(api_key)

    return api_key
