# app/services/usage_logger.py

import os
import time
import json
import redis

REDIS_URL = os.getenv("REDIS_URL")

# Redis is optional
redis_client = None

if REDIS_URL:
    redis_client = redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True
    )

USAGE_LOG_KEY = "usage:logs"


def log_usage(token: str, endpoint: str, details: str = ""):
    """
    Usage logger:
    - Stores structured logs in Redis list
    - Can be inspected later for analytics
    """

    # If Redis is unavailable, skip logging
    if redis_client is None:
        return

    entry = {
        "timestamp": time.time(),
        "token": token,
        "endpoint": endpoint,
        "details": details,
    }

    # Push to Redis list (most recent at head)
    redis_client.lpush(
        USAGE_LOG_KEY,
        json.dumps(entry)
    )