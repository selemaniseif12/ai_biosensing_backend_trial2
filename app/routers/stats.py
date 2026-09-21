from fastapi import APIRouter
from pydantic import BaseModel
import statistics

router = APIRouter(prefix="/stats", tags=["Statistics"])


# ---------------------------------------------------------
# GET: Basic info endpoint
# ---------------------------------------------------------
@router.get("/")
def stats_root():
    return {
        "message": "Statistics endpoints are working",
        "available_endpoints": [
            "/stats",
            "/stats/example",
            "/stats/basic"
        ]
    }


# ---------------------------------------------------------
# GET: Example statistics
# ---------------------------------------------------------
@router.get("/example")
def example_stats():
    values = [1, 2, 3, 4, 5]
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values)
    }


# ---------------------------------------------------------
# POST: User-provided statistics (your original endpoint)
# ---------------------------------------------------------
class StatsInput(BaseModel):
    values: list[float]


@router.post("/basic")
def basic_statistics(data: StatsInput):
    if len(data.values) == 0:
        return {"error": "values list cannot be empty"}

    return {
        "count": len(data.values),
        "mean": statistics.mean(data.values),
        "median": statistics.median(data.values),
        "min": min(data.values),
        "max": max(data.values)
    }
