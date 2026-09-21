from fastapi import APIRouter

# This router is intentionally disabled for deployment.
# All ML logic, CSV loading, and model calls have been removed.

router = APIRouter(prefix="/virus", tags=["Virus Multiclass"])

# ---------------------------------------------------------
# OFFLINE DASHBOARD DATA
# ---------------------------------------------------------
@router.post("/dashboard_data")
def dashboard_data():
    return {
        "status": "offline",
        "reason": "Virus Multiclass V7 model not deployed",
        "message": "dashboard_data endpoint is disabled for production."
    }

# ---------------------------------------------------------
# OFFLINE V7 PROBABILITIES ENDPOINT
# ---------------------------------------------------------
@router.post("/probabilities/v7")
def v7_probabilities(payload: dict):
    return {
        "status": "offline",
        "reason": "Virus Multiclass V7 model not deployed",
        "message": "probabilities/v7 endpoint is disabled for production."
    }
