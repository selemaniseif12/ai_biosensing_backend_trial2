from sqlalchemy.orm import Session
from app.models.measurement import Measurement
from app.schemas.measurements import MeasurementCreate, MeasurementUpdate


def get_measurements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Measurement).offset(skip).limit(limit).all()


def get_measurement(db: Session, measurement_id: int):
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()


def create_measurement(db: Session, data: MeasurementCreate):
    measurement = Measurement(
        customer_id=data.customer_id,
        frequency=data.frequency,
        amplitude=data.amplitude,
        phase=data.phase,
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


def update_measurement(db: Session, measurement_id: int, data: MeasurementUpdate):
    measurement = get_measurement(db, measurement_id)
    if not measurement:
        return None

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(measurement, field, value)

    db.commit()
    db.refresh(measurement)
    return measurement


def delete_measurement(db: Session, measurement_id: int):
    measurement = get_measurement(db, measurement_id)
    if not measurement:
        return False

    db.delete(measurement)
    db.commit()
    return True
