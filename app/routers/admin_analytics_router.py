from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import String

from app.dependencies.db import get_db

from app.models.analysis_log_model import AnalysisLog  # <-- FIXED

router = APIRouter(
    prefix="/analytics",
    tags=["Admin Analytics"]
)

@router.get("/logs")
def get_all_logs(db: Session = Depends(get_db)):
    logs = (
        db.query(AnalysisLog)
        .order_by(AnalysisLog.created_at.desc())
        .all()
    )
    return logs


@router.get("/logs/version/{version}")
def get_logs_by_version(version: str, db: Session = Depends(get_db)):
    logs = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.version == version)
        .order_by(AnalysisLog.created_at.desc())
        .all()
    )
    return logs


@router.get("/logs/date/{date}")
def get_logs_by_date(date: str, db: Session = Depends(get_db)):
    try:
        logs = (
            db.query(AnalysisLog)
            .filter(AnalysisLog.created_at.cast(String).like(f"{date}%"))
            .order_by(AnalysisLog.created_at.desc())
            .all()
        )
        return logs
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
