from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import requests
import joblib
import pandas as pd
import os
import time
import json

router = APIRouter()

BASE_URL = "http://127.0.0.1:8000"

# Lazy-loaded models and virus table
model_v2 = None
model_v6 = None
virus_lookup = None


def load_models():
    """Lazy-load v2 and v6 models only when needed."""
    global model_v2, model_v6

    if model_v2 is None:
        path = "models/model_v2_stepB.pkl"
        if os.path.exists(path):
            model_v2 = joblib.load(path)
        else:
            raise FileNotFoundError("model_v2_stepB.pkl not found. Train v2 first.")

    if model_v6 is None:
        path = "models/model_v6_stepB.pkl"
        if os.path.exists(path):
            model_v6 = joblib.load(path)
        else:
            raise FileNotFoundError("model_v6_stepB.pkl not found. Train v6 first.")


def load_virus_lookup():
    """Lazy-load virus lookup table only when needed."""
    global virus_lookup

    if virus_lookup is None:
        path = "ML Model Analyzer v6 Table.csv"
        if not os.path.exists(path):
            raise FileNotFoundError(
                "ML Model Analyzer v6 Table.csv not found. "
                "Place it in the project root or update the path."
            )

        df = pd.read_csv(path)
        df = df[["ID", "virus"]].drop_duplicates()
        virus_lookup = df.set_index("ID")["virus"].to_dict()


def get_device_sensitivity(device_id: int) -> float:
    """Fetch delta_m_fg from /device/all."""
    resp = requests.get(f"{BASE_URL}/device/all")
    resp.raise_for_status()
    devices = resp.json()

    for d in devices:
        if d["id"] == device_id:
            return d["sensitivity_fg"]

    raise ValueError(f"Device {device_id} not found")


@router.post("/detect/realtime")
def detect_realtime(
    model_version: str,
    virus_id: int,
    device_id: int,
    deposition_rate: float,
    temperature: float,
    humidity: float,
    flow_rate: float,
    time_to_detection: float,
    mass_of_virus_fg: float,
):
    load_models()
    load_virus_lookup()

    if model_version.lower() == "v2":
        model = model_v2
    elif model_version.lower() == "v6":
        model = model_v6
    else:
        return {"error": "Invalid model_version. Use 'v2' or 'v6'."}

    delta_m_fg = get_device_sensitivity(device_id)

    resp = requests.get(
        f"{BASE_URL}/sensor/simulate",
        params={"virus_id": virus_id, "device_id": device_id},
    )
    resp.raise_for_status()
    data = resp.json()

    measured_frequency_hz = data["measured_frequency_hz"]
    delta_f_hz = data["delta_f_hz"]
    noise_hz = data["noise_hz"]
    q_factor = data.get("q_factor", 100.0)
    harmonic_strength = data.get("harmonic_strength", 0.5)
    signal_to_noise_ratio = data.get("signal_to_noise_ratio", 20.0)
    allan_deviation = data.get("allan_deviation", 1e-8)

    features = [
        deposition_rate,
        temperature,
        humidity,
        flow_rate,
        time_to_detection,
        mass_of_virus_fg,
        device_id,
        delta_m_fg,
        measured_frequency_hz,
        delta_f_hz,
        noise_hz,
        q_factor,
        harmonic_strength,
        signal_to_noise_ratio,
        allan_deviation,
    ]

    predicted_id = int(model.predict([features])[0])
    predicted_name = virus_lookup.get(predicted_id, "Unknown Virus")

    return {
        "model_version": model_version,
        "predicted_virus_id": predicted_id,
        "predicted_virus_name": predicted_name,
        "device_id": device_id,
        "delta_m_fg": delta_m_fg,
        "measured_frequency_hz": measured_frequency_hz,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,
        "q_factor": q_factor,
        "harmonic_strength": harmonic_strength,
        "signal_to_noise_ratio": signal_to_noise_ratio,
        "allan_deviation": allan_deviation,
        "message": "Real-time detection completed using Step B physics.",
    }


# ⭐ NEW — LIVE STREAM DETECTION (continuous classification)
@router.get("/detect/live-stream")
def detect_live_stream(
    model_version: str,
    virus_id: int,
    device_id: int,
    interval: float = 1.0,   # seconds between readings
):
    load_models()
    load_virus_lookup()

    if model_version.lower() == "v2":
        model = model_v2
    elif model_version.lower() == "v6":
        model = model_v6
    else:
        return {"error": "Invalid model_version. Use 'v2' or 'v6'."}

    delta_m_fg = get_device_sensitivity(device_id)

    def event_stream():
        while True:
            resp = requests.get(
                f"{BASE_URL}/sensor/simulate",
                params={"virus_id": virus_id, "device_id": device_id},
            )
            resp.raise_for_status()
            data = resp.json()

            measured_frequency_hz = data["measured_frequency_hz"]
            delta_f_hz = data["delta_f_hz"]
            noise_hz = data["noise_hz"]
            q_factor = data.get("q_factor", 100.0)
            harmonic_strength = data.get("harmonic_strength", 0.5)
            signal_to_noise_ratio = data.get("signal_to_noise_ratio", 20.0)
            allan_deviation = data.get("allan_deviation", 1e-8)

            features = [
                0, 0, 0, 0, 0, 0,  # physical params not needed for streaming
                device_id,
                delta_m_fg,
                measured_frequency_hz,
                delta_f_hz,
                noise_hz,
                q_factor,
                harmonic_strength,
                signal_to_noise_ratio,
                allan_deviation,
            ]

            predicted_id = int(model.predict([features])[0])
            predicted_name = virus_lookup.get(predicted_id, "Unknown Virus")

            payload = {
                "predicted_virus_id": predicted_id,
                "predicted_virus_name": predicted_name,
                "measured_frequency_hz": measured_frequency_hz,
                "delta_f_hz": delta_f_hz,
                "noise_hz": noise_hz,
                "timestamp": time.time(),
            }

            yield f"data: {json.dumps(payload)}\n\n"
            time.sleep(interval)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
