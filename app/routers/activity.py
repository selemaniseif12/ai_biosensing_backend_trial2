# app/routers/activity.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)

@router.get("/status")
def activity_status():
    return {"message": "Activity dashboard is active"}
