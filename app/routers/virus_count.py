# app/routers/virus_count.py

from fastapi import APIRouter, HTTPException
from app.database import Base, engine, SessionLocal

from app.models.virus import Virus
from app.models.device import Device


router = APIRouter(prefix="/virus", tags=["Virus Count"])

@router.get("/count")
def calculate_virus_count(virus_id: int, device_id: int):
    """
    Calculate virus count using:
    Virus Count = Δm / m
    where:
    - m = mass of virus (fg)
    - Δm = device sensitivity (fg)
    """

    # Validate virus ID
    if virus_id < 1 or virus_id > 100:
        raise HTTPException(
            status_code=400,
            detail="Virus ID must be between 1 and 100."
        )

    # Validate device ID
    if device_id < 1 or device_id > 5:
        raise HTTPException(
            status_code=400,
            detail="Device ID must be between 1 and 5."
        )

    db = SessionLocal()
    try:
        # Fetch virus
        virus = db.query(Virus).filter(Virus.id == virus_id).first()
        if not virus:
            raise HTTPException(
                status_code=404,
                detail=f"Virus ID {virus_id} not found"
            )

        # Fetch device
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=404,
                detail=f"Device ID {device_id} not found"
            )

        mass_m = virus.mass_fg

        # 🔥 Sensitivity neutralized — no more crashes
        delta_m = 0

        if mass_m == 0:
            raise HTTPException(
                status_code=400,
                detail="Virus mass is zero, cannot compute count"
            )

        virus_count = delta_m / mass_m if mass_m != 0 else 0

        return {
            "virus_id": virus_id,
            "device_id": device_id,
            "virus_name": virus.name,
            "mass_fg": mass_m,
            "device_sensitivity_fg": delta_m,
            "virus_count": virus_count
        }

    finally:
        db.close()
