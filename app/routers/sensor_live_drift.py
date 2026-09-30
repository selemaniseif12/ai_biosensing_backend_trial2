from fastapi import APIRouter
import random

# NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage

# ⭐ REQUIRED — THIS WAS MISSING AND CAUSED THE CRASH
router = APIRouter(prefix="/sensor", tags=["Sensor Drift"])

BASE_F = 1693999.68345656012345

# Live state
current_second = 0
cumulative_drift = 0.0
start_t = 0
stop_t = 100
initialized = False


def tuned_step(threshold: float, window: int):
    """
    Uniform drift tuning:
    - Smaller drift for short windows
    - Slight damping for long windows
    - Micro-step drift for smooth spectrum
    """

    scale = 1.0

    if window <= 10:
        scale = 0.05
    elif window <= 20:
        scale = 0.08
    elif window <= 50:
        scale = 0.1
    elif window <= 100:
        scale = 0.15
    else:
        scale = 0.2

    step = random.uniform(-threshold, threshold) * scale
    return step


@router.get("/live_init")
def live_init(token: str = None, start_time: int = 0, stop_time: int = 100):
    """
    Initialize a new sweep:
    - reset drift
    - reset time
    - store start/stop time
    """

    # ⭐ RATE LIMITING (only if token provided)
    if token:
        rate_limit(token, endpoint="sensor_live_init")
        log_usage(
            token=token,
            endpoint="sensor_live_init",
            details=f"Init sweep start={start_time}, stop={stop_time}"
        )

    global current_second, cumulative_drift, start_t, stop_t, initialized

    start_t = start_time
    stop_t = stop_time

    current_second = start_t
    cumulative_drift = 0.0
    initialized = True

    return {
        "message": "Sweep initialized",
        "base_frequency_hz": BASE_F,
        "start_time": start_t,
        "stop_time": stop_t
    }


@router.get("/live_tick")
def live_tick(token: str = None, threshold: float = 0.1):
    """
    One live sample per second.
    Stops exactly at stop_time.
    After stop, next run starts at zero automatically.
    """

    # ⭐ RATE LIMITING (only if token provided)
    if token:
        rate_limit(token, endpoint="sensor_live_tick")
        log_usage(
            token=token,
            endpoint="sensor_live_tick",
            details=f"threshold={threshold}"
        )

    global current_second, cumulative_drift, start_t, stop_t, initialized

    # Auto-reset if frontend forgot to call /live_init
    if not initialized:
        current_second = 0
        cumulative_drift = 0.0
        start_t = 0
        stop_t = 100
        initialized = True

    # Stop condition
    if current_second > stop_t:
        initialized = False
        return {
            "done": True,
            "time_s": current_second,
            "base_frequency_hz": BASE_F,
            "measured_frequency_hz": BASE_F + cumulative_drift,
            "drift_hz": cumulative_drift,
            "message": "Sweep finished"
        }

    window = stop_t - start_t

    # Apply tuned drift
    step = tuned_step(threshold, window)

    # Slight damping
    cumulative_drift *= 0.995

    cumulative_drift += step

    measured = BASE_F + cumulative_drift

    response = {
        "done": False,
        "time_s": current_second,
        "base_frequency_hz": BASE_F,
        "measured_frequency_hz": measured,
        "drift_hz": cumulative_drift,
        "threshold": threshold
    }

    current_second += 1
    return response
