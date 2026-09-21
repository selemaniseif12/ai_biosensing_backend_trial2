from sqlalchemy.orm import Session
from app.models.usage import UsageLog
from app.schemas.usage import UsageCreate


# ---------------------------------------------------------
# List all usage logs
# ---------------------------------------------------------
def service_list_usage_logs(db: Session):
    return db.query(UsageLog).all()


# ---------------------------------------------------------
# Create new usage log
# Accepts both Pydantic model and raw dict (from ML/Virus/Compare APIs)
# ---------------------------------------------------------
def service_create_usage_log(db: Session, data):
    # If data is a Pydantic model, convert to dict
    if isinstance(data, UsageCreate):
        payload = data.dict()
    else:
        payload = data  # raw dict from API services

    log = UsageLog(**payload)

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


# ---------------------------------------------------------
# Get usage log by ID
# ---------------------------------------------------------
def service_get_usage_log(db: Session, usage_id: int):
    return db.query(UsageLog).filter(UsageLog.id == usage_id).first()


# ---------------------------------------------------------
# Delete usage log
# ---------------------------------------------------------
def service_delete_usage_log(db: Session, usage_id: int):
    log = service_get_usage_log(db, usage_id)
    if not log:
        return False

    db.delete(log)
    db.commit()
    return True
