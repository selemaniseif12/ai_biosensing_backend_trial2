# ============================================================
# File: routers/multiclass_dashboard_v6.py
# Description: Duplicate V6 dashboard endpoint (line charts + table)
# Author: Selemani
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np

# ⭐ Correct import — import module, not model_v6 directly
import app.routers.ml_multiclassify_router as mlrouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard V6"])


class DashboardV6Request(BaseModel):
    features: list[float]
    input_frequency_mhz: float | None = None
    threshold_hz: float = 0.0


@router.post("/v6")
def dashboard_v6(req: DashboardV6Request):
    """
    Clean V6 dashboard endpoint.
    EXACT duplicate of V6 classifier structure.
    """

    # ⭐ Load models properly
    mlrouter.load_models()

    # Extract features EXACTLY like V6
    base_frequency_hz = req.features[0] if len(req.features) > 0 else None
    measured_frequency_hz = req.features[6] if len(req.features) > 6 else None

    # Handle input frequency override EXACTLY like V6
    input_frequency_mhz = req.input_frequency_mhz
    input_frequency_hz = None
    if input_frequency_mhz is not None:
        input_frequency_hz = input_frequency_mhz * 1_000_000.0
        if len(req.features) >= 7:
            req.features[6] = input_frequency_hz
            measured_frequency_hz = input_frequency_hz

    # ⭐ Use dynamically loaded model
    probs = mlrouter.model_v6.predict_proba([req.features])[0]
    classes = mlrouter.model_v6.classes_

    # Build results EXACTLY like V6
    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    # Apply threshold EXACTLY like V6
    if req.threshold_hz > 0:
        filtered_results = {k: v for k, v in sorted_results.items() if v >= req.threshold_hz}
    else:
        filtered_results = sorted_results

    # Build masses + names EXACTLY like V6
    sorted_masses = {k: mlrouter.masses.get(k) for k in filtered_results.keys()}
    sorted_names = {k: mlrouter.virus_names.get(k) for k in filtered_results.keys()}

    # Build chart data EXACTLY like V6
    chart_data = [
        {"virus_id": int(k), "probability": float(filtered_results[k]), "mass_fg": sorted_masses[k]}
        for k in filtered_results.keys()
    ]

    # Build mass chart EXACTLY like V6
    chart_mass_data = [
        {"mass_fg": sorted_masses[k], "probability": float(filtered_results[k])}
        for k in filtered_results.keys()
    ]

    return {
        "model_version": "v6-dashboard-duplicate",
        "input_features": req.features,
        "threshold_hz": req.threshold_hz,

        "base_frequency_hz": base_frequency_hz,
        "measured_frequency_hz": measured_frequency_hz,

        "input_frequency_mhz": input_frequency_mhz,
        "input_frequency_hz": input_frequency_hz,

        "virus_probabilities": filtered_results,
        "virus_masses_fg": sorted_masses,
        "virus_names": sorted_names,

        "chart_data": chart_data,
        "chart_mass_data": chart_mass_data,

        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "V6 dashboard duplicate executed successfully."
    }
