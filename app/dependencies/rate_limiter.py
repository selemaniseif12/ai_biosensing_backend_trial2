import time
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.api_key import APIKey

# In-memory store: { "api_key": [timestamps...] }
RATE_LIMIT_STORE = {}

# Configurable limits
REQUESTS_PER_MINUTE_PER_KEY = 20
REQUESTS_PER_MINUTE_PER_CUSTOMER = 100


def rate_limit(api_key: APIKey, db: Session):
    now = time.time()

    # -----------------------------
    # Per-key rate limiting
    # -----------------------------
    key_bucket = RATE_LIMIT_STORE.setdefault(api_key.key, [])
    key_bucket[:] = [t for t in key_bucket if now - t < 60]

    if len(key_bucket) >= REQUESTS_PER_MINUTE_PER_KEY:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for this API key"
        )

    key_bucket.append(now)

    # -----------------------------
    # Per-customer rate limiting
    # -----------------------------
    customer_keys = db.query(APIKey).filter(APIKey.customer_id == api_key.customer_id).all()

    total_requests = 0
    for k in customer_keys:
        bucket = RATE_LIMIT_STORE.setdefault(k.key, [])
        bucket[:] = [t for t in bucket if now - t < 60]
        total_requests += len(bucket)

    if total_requests >= REQUESTS_PER_MINUTE_PER_CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for this customer"
        )

    return True
