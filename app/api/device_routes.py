# ============================================================
# File: api/device_routes.py
# Description: FastAPI router for device retrieval endpoints.
# Author: Selemani
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ✅ Import the REAL database dependency
from app.database import get_db

# ✅ Import your Device model
from app.models.device import Device


router = APIRouter()

@router.get("/devices")
def get_all_devices(db: Session = Depends(get_db)):
    """
    Returns all devices from the database.
    """
    return db.query(Device).all()
