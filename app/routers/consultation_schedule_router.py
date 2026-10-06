from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.consultations import Consultation
from app.models.team_model import Team
from app.models.consultation_schedule import ConsultationSchedule

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage
from app.services.email_service import send_email   # <-- Gmail SMTP sender

router = APIRouter(prefix="/consultations", tags=["Consultation Scheduling"])


# ---------------------------------------------------------
# Helper: Convert ORM schedule → JSON-safe dict
# ---------------------------------------------------------
def schedule_to_dict(schedule: ConsultationSchedule, consultation: Consultation):
    return {
        "id": schedule.id,
        "title": consultation.topic,
        "date": schedule.scheduled_time.date().isoformat() if schedule.scheduled_time else None,
        "time": schedule.scheduled_time.strftime("%H:%M") if schedule.scheduled_time else None,
        "platform": "teams" if "teams" in (schedule.meeting_link or "").lower() else "google",
        "participants": getattr(consultation, "user_email", None),
        "meeting_link": schedule.meeting_link
    }


# ---------------------------------------------------------
# 1. Schedule a consultation
# ---------------------------------------------------------
@router.post("/{consultation_id}/schedule")
def schedule_consultation(
    consultation_id: int,
    scheduled_time: datetime,
    meeting_link: str = None,
    token: str = "",
    db: Session = Depends(get_db)
):
    """
    Schedule a consultation.
    - Rate-limited
    - Usage logged
    """

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="consultation_schedule_create")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="consultation_schedule_create",
        details=f"Scheduled consultation {consultation_id}"
    )

    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    if not consultation.team_id:
        raise HTTPException(status_code=400, detail="Assign a team before scheduling")

    schedule = ConsultationSchedule(
        consultation_id=consultation_id,
        team_id=consultation.team_id,
        scheduled_time=scheduled_time,
        meeting_link=meeting_link
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    # ⭐ EMAIL NOTIFICATIONS (Gmail SMTP)
    user_email = getattr(consultation, "user_email", None)

    if user_email:
        send_email(
            email_to=user_email,
            subject="Your Consultation Has Been Scheduled",
            body=(
                f"Hello,\n\n"
                f"Your consultation has been scheduled.\n\n"
                f"Topic: {consultation.topic}\n"
                f"Date: {scheduled_time.date().isoformat()}\n"
                f"Time: {scheduled_time.strftime('%H:%M')}\n"
                f"Meeting Link: {meeting_link}\n\n"
                f"Thank you."
            )
        )

    # ⭐ ADMIN NOTIFICATION (you)
    send_email(
        email_to="selemaniseif12@yahoo.com",
        subject="New Consultation Scheduled",
        body=(
            f"A new consultation has been scheduled.\n\n"
            f"Consultation ID: {consultation_id}\n"
            f"User Email: {user_email}\n"
            f"Topic: {consultation.topic}\n"
            f"Date: {scheduled_time.date().isoformat()}\n"
            f"Time: {scheduled_time.strftime('%H:%M')}\n"
            f"Meeting Link: {meeting_link}\n"
        )
    )

    return schedule_to_dict(schedule, consultation)


# ---------------------------------------------------------
# 2. Get all scheduled consultations (dashboard)
# ---------------------------------------------------------
@router.get("/scheduled")
def get_all_scheduled(token: str = "", db: Session = Depends(get_db)):
    """
    Get all scheduled consultations.
    - Rate-limited
    - Usage logged
    """

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="consultation_schedule_list")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="consultation_schedule_list",
        details="Fetched all scheduled consultations"
    )

    schedules = db.query(ConsultationSchedule).all()
    result = []

    for s in schedules:
        consultation = db.query(Consultation).filter(Consultation.id == s.consultation_id).first()
        if consultation:
            result.append(schedule_to_dict(s, consultation))

    return result
