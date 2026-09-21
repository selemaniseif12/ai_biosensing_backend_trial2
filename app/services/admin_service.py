from sqlalchemy.orm import Session
from app.models.customers import Customer
from app.models.detection import Detection


def list_customers(db: Session):
    return db.query(Customer).all()


def list_detections(db: Session):
    return db.query(Detection).all()
