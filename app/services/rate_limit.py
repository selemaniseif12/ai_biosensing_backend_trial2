# Trigger redeploy
import os
import time
from fastapi import HTTPException
import redis

# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set in environment")

# Single Redis client with connection pool
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Strict config
PER_TOKEN_DEFAULT_LIMIT = 20        # generic endpoints
PER_TOKEN_DEFAULT_WINDOW = 60       # seconds

GLOBAL_LIMIT = 100                  # all requests per minute
GLOBAL_WINDOW = 60                  # seconds


def _token_key(token: str, endpoint: str) -> str:
    return f"rl:token:{token}:{endpoint}"


def _global_key() -> str:
    return "rl:global"


def _check_window(key: str, now: int, window_seconds: int, limit: int) -> bool:
    """
    Sliding window using Redis sorted set:
    - members: timestamps
    - score: timestamps
    """
    pipe = redis_client.pipeline()

    # Add current timestamp
    pipe.zadd(key, {str(now): now})

    # Remove entries older than window
    pipe.zremrangebyscore(key, 0, now - window_seconds)

    # Count remaining
    pipe.zcard(key)

    # Ensure key expires if idle
    pipe.expire(key, window_seconds)

    _, _, count, _ = pipe.execute()

    return count <= limit


def rate_limit(
    token: str,
    endpoint: str,
    limit: int = PER_TOKEN_DEFAULT_LIMIT,
    window_seconds: int = PER_TOKEN_DEFAULT_WINDOW,
):
    """
    Redis-backed sliding window rate limiting:
    - Per-token + per-endpoint
    - Global limit
    - Strict defaults
    """

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    now = int(time.time())

    # Per-token + endpoint key
    token_key = _token_key(token, endpoint)

    # Check per-token limit
    ok_token = _check_window(token_key, now, window_seconds, limit)
    if not ok_token:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded for {endpoint}. Try again later.",
        )

    # Check global limit
    global_key = _global_key()
    ok_global = _check_window(global_key, now, GLOBAL_WINDOW, GLOBAL_LIMIT)
    if not ok_global:
        raise HTTPException(
            status_code=429,
            detail="Global rate limit exceeded. Try again later.",
        )
