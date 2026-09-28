from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from firebase_admin import auth
import asyncio, json, time

from app.database import Base, engine, SessionLocal
from app.models.sensor_history import SensorHistory

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage

router = APIRouter()


# ---------------------------------------------------------
# Firebase Token Verification (Query Param for SSE)
# ---------------------------------------------------------
async def verify_firebase_token(token: str = Query(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")


# ---------------------------------------------------------
# Save Sensor Data to Database
# ---------------------------------------------------------
async def save_history(device_id: str, sensor_type: str, value: float):
    db = SessionLocal()
    try:
        entry = SensorHistory(
            device_id=device_id,
            sensor_type=sensor_type,
            value=value
        )
        db.add(entry)
        db.commit()
    finally:
        db.close()


# ---------------------------------------------------------
# Sensor Generators (store + stream)
# ---------------------------------------------------------
async def generate_temperature(device_id="global"):
    while True:
        value = 20 + (time.time() % 5)
        await save_history(device_id, "temperature", value)
        yield f"data: {json.dumps({'timestamp': time.time(), 'value': value})}\n\n"
        await asyncio.sleep(0.2)


async def generate_humidity(device_id="global"):
    while True:
        value = 40 + (time.time() % 10)
        await save_history(device_id, "humidity", value)
        yield f"data: {json.dumps({'timestamp': time.time(), 'value': value})}\n\n"
        await asyncio.sleep(0.2)


async def generate_pressure(device_id="global"):
    while True:
        value = 1000 + (time.time() % 20)
        await save_history(device_id, "pressure", value)
        yield f"data: {json.dumps({'timestamp': time.time(), 'value': value})}\n\n"
        await asyncio.sleep(0.2)


async def generate_ecg(device_id="global"):
    while True:
        value = round(0.5 + (time.time() % 1), 3)
        await save_history(device_id, "ecg", value)
        yield f"data: {json.dumps({'timestamp': time.time(), 'value': value})}\n\n"
        await asyncio.sleep(0.05)


# ---------------------------------------------------------
# Global Sensor Streams (no device ID)
# ---------------------------------------------------------
@router.get("/stream/sensor/temperature")
async def stream_temperature(token: str, user=Depends(verify_firebase_token)):

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="stream_temperature")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="stream_temperature",
        details="Global temperature stream"
    )

    return StreamingResponse(
        generate_temperature("global"),
        media_type="text/event-stream"
    )


@router.get("/stream/sensor/humidity")
async def stream_humidity(token: str, user=Depends(verify_firebase_token)):

    rate_limit(token, endpoint="stream_humidity")

    log_usage(
        token=token,
        endpoint="stream_humidity",
        details="Global humidity stream"
    )

    return StreamingResponse(
        generate_humidity("global"),
        media_type="text/event-stream"
    )


@router.get("/stream/sensor/pressure")
async def stream_pressure(token: str, user=Depends(verify_firebase_token)):

    rate_limit(token, endpoint="stream_pressure")

    log_usage(
        token=token,
        endpoint="stream_pressure",
        details="Global pressure stream"
    )

    return StreamingResponse(
        generate_pressure("global"),
        media_type="text/event-stream"
    )


@router.get("/stream/sensor/ecg")
async def stream_ecg(token: str, user=Depends(verify_firebase_token)):

    rate_limit(token, endpoint="stream_ecg")

    log_usage(
        token=token,
        endpoint="stream_ecg",
        details="Global ECG stream"
    )

    return StreamingResponse(
        generate_ecg("global"),
        media_type="text/event-stream"
    )


# ---------------------------------------------------------
# Device-Specific Sensor Streams
# ---------------------------------------------------------
@router.get("/stream/device/{device_id}/sensor/{sensor_type}")
async def stream_device_sensor(
    device_id: str,
    sensor_type: str,
    token: str,
    user=Depends(verify_firebase_token)
):

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint=f"stream_device_{sensor_type}")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint=f"stream_device_{sensor_type}",
        details=f"Device={device_id}, sensor={sensor_type}"
    )

    generators = {
        "temperature": generate_temperature,
        "humidity": generate_humidity,
        "pressure": generate_pressure,
        "ecg": generate_ecg,
    }

    if sensor_type not in generators:
        raise HTTPException(status_code=404, detail="Unknown sensor type")

    return StreamingResponse(
        generators[sensor_type](device_id),
        media_type="text/event-stream"
    )
