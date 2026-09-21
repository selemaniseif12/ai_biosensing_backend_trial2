# app/crud/ml_logging.py
from sqlalchemy.orm import Session
from app.models.ml_log import MLLog

def create_log(db: Session, model_id: int, run_id: str, status: str = "pending", duration: float = None, accuracy: float = None):
    log = MLLog(
        model_id=model_id,
        run_id=run_id,
        status=status,
        duration=duration,
        accuracy=accuracy
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_log(db: Session, log_id: int):
    return db.query(MLLog).filter(MLLog.id == log_id).first()

def get_logs_by_model(db: Session, model_id: int):
    return db.query(MLLog).filter(MLLog.model_id == model_id).all()

def update_log_status(db: Session, log_id: int, status: str):
    log = get_log(db, log_id)
    if not log:
        return None
    log.status = status
    db.commit()
    db.refresh(log)
    return log

def delete_log(db: Session, log_id: int):
    log = get_log(db, log_id)
    if log:
        db.delete(log)
        db.commit()
    return log
