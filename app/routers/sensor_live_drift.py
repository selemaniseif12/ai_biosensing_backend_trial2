@router.get("/live_init")
def live_init(token: str = None, start_time: int = 0, stop_time: int = 100):

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

    if token:
        rate_limit(token, endpoint="sensor_live_tick")
        log_usage(
            token=token,
            endpoint="sensor_live_tick",
            details=f"threshold={threshold}"
        )

    global current_second, cumulative_drift, start_t, stop_t, initialized

    if not initialized:
        current_second = 0
        cumulative_drift = 0.0
        start_t = 0
        stop_t = 100
        initialized = True

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
    step = tuned_step(threshold, window)

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
