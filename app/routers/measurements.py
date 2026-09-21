from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db

from app.schemas.measurements import MeasurementCreate, MeasurementUpdate
from app.services.measurement_service import (
    create_measurement,
    get_measurement,
    get_all_measurements,
    update_measurement,
    delete_measurement,
)

router = APIRouter(tags=["Measurements"])


@router.post("/")
def create(data: MeasurementCreate, db: Session = Depends(get_db)):
    measurement = create_measurement(data, db)
    if not measurement:
        raise HTTPException(status_code=404, detail="Device not found")
    return measurement


@router.get("/{measurement_id}")
def read(measurement_id: int, db: Session = Depends(get_db)):
    measurement = get_measurement(measurement_id, db)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    return get_all_measurements(db)


@router.put("/{measurement_id}")
def update(measurement_id: int, data: MeasurementUpdate, db: Session = Depends(get_db)):
    updated = update_measurement(measurement_id, data, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return updated


@router.delete("/{measurement_id}")
def delete(measurement_id: int, db: Session = Depends(get_db)):
    deleted = delete_measurement(measurement_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return {"deleted": True}
