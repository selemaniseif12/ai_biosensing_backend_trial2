# app/analyzer_v6_loader.py

from app.ml.analyzer_v6_model import analyzer_v6
from app.models.database import SessionLocal
from app.models.models import AnalyzerV6Log   # <-- FIXED IMPORT


def log_v6_prediction(payload: dict, prediction: float):
    db = SessionLocal()
    try:
        log_entry = AnalyzerV6Log(
            device_id=payload["device_id"],
            virus=payload["virus"],
            deposition_rate=payload["deposition_rate"],
            temperature=payload["temperature"],
            humidity=payload["humidity"],
            flow_rate=payload["flow_rate"],
            mass_of_virus=payload["mass_of_virus"],
            predicted_time_to_detection=prediction,
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print("Logging error:", e)
    finally:
        db.close()


def predict(payload: dict) -> float:
    features = [
        payload["deposition_rate"],
        payload["temperature"],
        payload["humidity"],
        payload["flow_rate"],
        payload["mass_of_virus"],
    ]

    prediction = float(analyzer_v6.predict([features])[0])

    log_v6_prediction(payload, prediction)

    return prediction
