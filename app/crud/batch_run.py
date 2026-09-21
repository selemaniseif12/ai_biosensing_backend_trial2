from sqlalchemy.orm import Session
from app.models.batch_run import BatchRun

def create_batch_run(db: Session, data: dict):
    record = BatchRun(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
