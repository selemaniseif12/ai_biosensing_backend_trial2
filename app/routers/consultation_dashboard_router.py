from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consultations import Consultation
from app.models.consultation_schedule import ConsultationSchedule

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage

router = APIRouter(prefix="/consultations/dashboard", tags=["Consultation Dashboard"])


# ---------------------------------------------------------
# Helper: Convert ORM objects → JSON-safe dict
# ---------------------------------------------------------
def consultation_to_dict(c: Consultation, schedule: ConsultationSchedule | None):
    return {
        "id": c.id,
        "topic": c.topic,
        "email": getattr(c, "user_email", None),
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
def get_upcoming_consultations(token: str = "", db: Session = Depends(get_db)):
    """
    Dashboard: upcoming consultations.
    - Rate-limited
    - Usage logged
    """

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="consultation_dashboard_upcoming")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="consultation_dashboard_upcoming",
        details="Fetched upcoming consultations dashboard"
    )

    consultations = db.query(Consultation).all()
    result = []

    for c in consultations:
        schedule = db.query(ConsultationSchedule).filter(
            ConsultationSchedule.consultation_id == c.id
        ).first()

        result.append(consultation_to_dict(c, schedule))

    return result
