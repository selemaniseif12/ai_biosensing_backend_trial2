from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_core import get_db
from app.models.models import Analyzer1Device, Measurement

router = APIRouter(
    prefix="/analyzer_v1",
    tags=["Analyzer v1"]
)

# -----------------------------
# QCM / Sauerbrey Calculations
# -----------------------------
def compute_delta_f(device: Analyzer1Device, measured_frequency: float):
    return device.frequency_mhz - measured_frequency

def compute_mass_change(device: Analyzer1Device, delta_f: float):
    # Sauerbrey-like proportionality using stored m_g
    # m_g is the mass sensitivity constant for the device
    if device.frequency_mhz == 0:
        return 0
    return device.m_g * (delta_f / device.frequency_mhz)


# -----------------------------
# Analyzer Endpoint
# -----------------------------
@router.post("/measure")
def analyze_and_save(
    device_id: int,
    measured_frequency_mhz: float,
    sample_id: int = 1,
    db: Session = Depends(get_db)
):
    # 1. Load device
    device = db.query(Analyzer1Device).filter_by(device_id=device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # 2. Compute Δf
    delta_f = compute_delta_f(device, measured_frequency_mhz)

    # 3. Compute Δm (mass change)
    delta_m = compute_mass_change(device, delta_f)

    # 4. Save measurement to database
    measurement = Measurement(
        sample_id=sample_id,
        device_id=device_id,
        frequency_mhz=measured_frequency_mhz,
        delta_f_mhz=delta_f,
        m_g=delta_m
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    # 5. Return full device + measurement data
    return {
        "device_id": device.device_id,
        "sample_id": sample_id,
        "measured_frequency_mhz": measured_frequency_mhz,
        "device_frequency_mhz": device.frequency_mhz,
        "delta_f_mhz": delta_f,
        "delta_m_g": delta_m,
        "device_parameters": {
            "center_electrode_mm": device.center_electrode_mm,
            "diameter_mm": device.diameter_mm,
            "chromium_nm": device.chromium_nm,
            "gold_nm": device.gold_nm,
            "thickness_mm": device.thickness_mm,
        },
        "saved_measurement_id": measurement.id
    }
