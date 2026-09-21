from fastapi import APIRouter
import joblib
import pandas as pd

router = APIRouter()

# Load Step B models
model_v2 = joblib.load("models/model_v2_stepB.pkl")
model_v6 = joblib.load("models/model_v6_stepB.pkl")

# Virus lookup table (you can replace with DB if needed)
virus_lookup = pd.read_csv("ML Model Analyzer v6 Table.csv")
virus_lookup = virus_lookup[["ID", "virus"]].drop_duplicates()
virus_lookup = virus_lookup.set_index("ID")["virus"].to_dict()


@router.post("/classify/stepB")
def classify_stepB(
    model_version: str,
    virus_id: int,
    device_id: int,
    deposition_rate: float,
    temperature: float,
    humidity: float,
    flow_rate: float,
    time_to_detection: float,
    mass_of_virus_fg: float,
    delta_m_fg: float,
    measured_frequency_hz: float,
    delta_f_hz: float,
    noise_hz: float,
    q_factor: float,
    harmonic_strength: float,
    signal_to_noise_ratio: float,
    allan_deviation: float,
):
    """
    Step B physics-based classification endpoint.
    Uses v2 or v6 model to classify virus based on sensor physics.
    """

    # Select model
    if model_version.lower() == "v2":
        model = model_v2
    elif model_version.lower() == "v6":
        model = model_v6
    else:
        return {"error": "Invalid model version. Use 'v2' or 'v6'."}

    # Build Step B feature vector
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

    # Predict
    predicted_id = int(model.predict([features])[0])
    predicted_name = virus_lookup.get(predicted_id, "Unknown Virus")

    return {
        "model_version": model_version,
        "predicted_virus_id": predicted_id,
        "predicted_virus_name": predicted_name,
        "input_delta_f_hz": delta_f_hz,
        "input_delta_m_fg": delta_m_fg,
        "message": "Classification completed using Step B physics model."
    }
