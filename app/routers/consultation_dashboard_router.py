from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consultations import Consultation
from app.models.consultation_schedule import ConsultationSchedule

router = APIRouter(prefix="/consultations/dashboard", tags=["Consultation Dashboard"])


# ---------------------------------------------------------
# Helper: Convert ORM objects → JSON-safe dict
# ---------------------------------------------------------
def consultation_to_dict(c: Consultation, schedule: ConsultationSchedule | None):
    return {
        "id": c.id,
        "topic": c.topic,
        "email": getattr(c, "user_email", None),  # safe access
        "status": c.status,
        "scheduled": bool(schedule),
        "scheduled_time": (
            schedule.scheduled_time.isoformat() if schedule and schedule.scheduled_time else None
        ),
        "meeting_link": schedule.meeting_link if schedule else None
    }


# ---------------------------------------------------------
# Upcoming consultations dashboard
# ---------------------------------------------------------
@router.get("/upcoming")
def get_upcoming_consultations(db: Session = Depends(get_db)):
    consultations = db.query(Consultation).all()
    result = []

    for c in consultations:
        schedule = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.consultation_id == c.id
        ).first()

        result.append(consultation_to_dict(c, schedule))

    return result
