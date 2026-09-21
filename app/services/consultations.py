from sqlalchemy.orm import Session
from app.models.consultations import Consultation
from app.models.team_model import Team


def list_consultations(db: Session):
    return db.query(Consultation).all()


def get_consultation(db: Session, consultation_id: int):
    return db.query(Consultation).filter(Consultation.id == consultation_id).first()


def update_status(db: Session, consultation_id: int, status: str):
    consultation = get_consultation(db, consultation_id)
    if consultation:
        consultation.status = status
        db.commit()
        db.refresh(consultation)
    return consultation


def overview(db: Session):
    consultations = db.query(Consultation).all()

    upcoming = [c for c in consultations if c.status == "scheduled"]
    completed = [c for c in consultations if c.status == "completed"]
    cancelled = [c for c in consultations if c.status == "cancelled"]

    return {
        "upcoming": upcoming,
        "completed": completed,
        "cancelled": cancelled
    }
