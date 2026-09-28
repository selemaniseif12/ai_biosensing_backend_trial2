# app/services/usage_logger.py

import time

def log_usage(token: str, endpoint: str, details: str = ""):
    """
    Simple usage logger.
    For now it prints to console.
    Later you can store in DB.
    """
    print({
        "timestamp": time.time(),
        "token": token,
        "endpoint": endpoint,
        "details": details
    })
