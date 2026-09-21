from sqlalchemy.orm import Session
from app.models.models import Measurement, Analyzer1Device


def create_measurement(data, db: Session):
    device = db.query(Analyzer1Device).filter(
        Analyzer1Device.device_id == data.device_id
    ).first()

    if not device:
        return None

    measurement = Measurement(
        sample_id=data.sample_id,
        device_id=data.device_id,
        frequency_mhz=data.frequency_mhz,
        delta_f_mhz=data.delta_f_mhz,
        m_g=data.m_g,
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


def get_measurement(measurement_id: int, db: Session):
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()


def get_all_measurements(db: Session):
    return db.query(Measurement).all()


def update_measurement(measurement_id: int, data, db: Session):
    measurement = get_measurement(measurement_id, db)
    if not measurement:
        return None

    if data.frequency_mhz is not None:
        measurement.frequency_mhz = data.frequency_mhz
    if data.delta_f_mhz is not None:
        measurement.delta_f_mhz = data.delta_f_mhz
    if data.m_g is not None:
        measurement.m_g = data.m_g

    db.commit()
    db.refresh(measurement)
    return measurement


def delete_measurement(measurement_id: int, db: Session):
    measurement = get_measurement(measurement_id, db)
    if not measurement:
        return None

    db.delete(measurement)
    db.commit()
    return True
