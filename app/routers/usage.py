from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Correct import path
from app.db.database import get_db

from app.schemas.usage import UsageCreate
from app.services.usage_service import (
    service_list_usage_logs,
    service_create_usage_log,
    service_get_usage_log,
    service_delete_usage_log,
)

router = APIRouter(
    prefix="/usage",
    tags=["Usage Logs"]
)

# ---------------------------------------------------------
# List all usage logs
# ---------------------------------------------------------
@router.get("/")
def list_usage_logs(db: Session = Depends(get_db)):
    return service_list_usage_logs(db)

# ---------------------------------------------------------
# Create new usage log
# ---------------------------------------------------------
@router.post("/")
def create_usage_log(data: UsageCreate, db: Session = Depends(get_db)):
    return service_create_usage_log(db, data)

# ---------------------------------------------------------
# Read usage log by ID
# ---------------------------------------------------------
@router.get("/{usage_id}")
def read_usage_log(usage_id: int, db: Session = Depends(get_db)):
    log = service_get_usage_log(db, usage_id)
    if not log:
        raise HTTPException(status_code=404, detail="Usage log not found")
    return log

# ---------------------------------------------------------
# Delete usage log
# ---------------------------------------------------------
@router.delete("/{usage_id}")
def delete_usage_log(usage_id: int, db: Session = Depends(get_db)):
    return service_delete_usage_log(db, usage_id)
