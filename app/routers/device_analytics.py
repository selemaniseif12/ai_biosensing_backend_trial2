from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal

from app.models.models import Device  # adjust if needed

router = APIRouter(prefix="/devices", tags=["Device Analytics"])

class DeviceAnalytics(BaseModel):
    status_counts: Dict[str, int]
    per_customer: Dict[str, int]

@router.get("/analytics", response_model=DeviceAnalytics)
def get_device_analytics():
    db: Session = SessionLocal()
    devices = db.query(Device).all()
    db.close()

    status_counts = {}
    per_customer = {}

    for d in devices:
        status_counts[d.status] = status_counts.get(d.status, 0) + 1
        email = getattr(d, "customer_email", "Unknown")
        per_customer[email] = per_customer.get(email, 0) + 1

    return DeviceAnalytics(
        status_counts=status_counts,
        per_customer=per_customer
    )
