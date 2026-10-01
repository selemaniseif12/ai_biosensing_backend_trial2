# app/services/usage_logger.py

import os
import time
import json
import redis

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set in environment")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

USAGE_LOG_KEY = "usage:logs"


def log_usage(token: str, endpoint: str, details: str = ""):
    """
    Usage logger:
    - Stores structured logs in Redis list
    - Can be inspected later for analytics
    """

    entry = {
        "timestamp": time.time(),
        "token": token,
        "endpoint": endpoint,
        "details": details,
    }

    # Push to Redis list (most recent at head)
    redis_client.lpush(USAGE_LOG_KEY, json.dumps(entry))
