# app/services/rate_limit.py

import time
from fastapi import HTTPException

# Simple in-memory rate limit store
RATE_LIMIT_STORE = {}

def rate_limit(token: str, endpoint: str, limit: int = 20, window_seconds: int = 60):
    """
    Basic rate limiting:
    - token identifies the user
    - endpoint identifies the API route
    - limit = max requests allowed
    - window_seconds = time window
    """

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    key = f"{token}:{endpoint}"
    now = time.time()

    if key not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[key] = []

    # Keep only recent timestamps
    RATE_LIMIT_STORE[key] = [
        ts for ts in RATE_LIMIT_STORE[key]
        if now - ts < window_seconds
    ]

    # Check limit
    if len(RATE_LIMIT_STORE[key]) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded for {endpoint}. Try again later."
        )

    # Add new timestamp
    RATE_LIMIT_STORE[key].append(now)
