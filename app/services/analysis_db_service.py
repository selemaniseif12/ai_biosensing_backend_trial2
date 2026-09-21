# app/services/analysis_db_service.py

from sqlalchemy.orm import Session
from app.models.analysis_result import AnalysisResult

def save_analysis_result(db: Session, data: dict):
    record = AnalysisResult(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
