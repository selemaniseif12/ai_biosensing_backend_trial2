from fastapi import APIRouter
import json
import os

router = APIRouter(prefix="/versioning", tags=["Model Versioning"])

META_PATH = "app/models/virus_multiclassify_V7_175_meta.json"

@router.get("/v7")
def get_version_v7():
    if not os.path.exists(META_PATH):
        return {"error": "Metadata file not found"}

    with open(META_PATH, "r") as f:
        metadata = json.load(f)

    return {
        "model_name": "Virus Multi-classify V7-175",
        "dataset_size": "175 samples",
        "training_status": "Training Completed",
        "accuracy": round(metadata.get("accuracy", 0) * 100, 2),
        "loss": "N/A (RandomForest Model)",
        "last_training_date": "2026-08-04",
        "epochs": "N/A",
        "training_time": "~3 seconds",
        "version": "V7-175",
        "parameters": metadata.get("parameters", {}),
        "base_frequency_hz": metadata.get("base_frequency_hz", None),
        "sensor_feature": metadata.get("sensor_feature", None),
        "logs": [
            "Feature Engineering Completed",
            "RandomForest Model Trained (800 trees)",
            "Sensor Drift Compensation Enabled",
            f"Final Accuracy: {round(metadata.get('accuracy', 0) * 100, 2)}%"
        ]
    }
