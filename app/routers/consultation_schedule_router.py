from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.consultations import Consultation
from app.models.team_model import Team
from app.models.consultation_schedule import ConsultationSchedule
from app.models.notification import Notification

# ⭐ NEW IMPORT — Meeting Email Sender
from app.services.meeting_email_service import send_meeting_email

router = APIRouter(prefix="/consultations", tags=["Consultation Scheduling"])


# ---------------------------------------------------------
# Schedule a consultation
# ---------------------------------------------------------
@router.post("/{consultation_id}/schedule")
def schedule_consultation(
    consultation_id: int,
    scheduled_time: datetime,
    meeting_link: str = None,
    db: Session = Depends(get_db)
):
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

    # ⭐ NEW — Send meeting email notification
    try:
        send_meeting_email(
            to_email=consultation.user_email,
            meeting_link=meeting_link,
            date=schedule.scheduled_time.date().isoformat(),
            time=schedule.scheduled_time.strftime("%H:%M"),
            topic=consultation.topic
        )
    except Exception as e:
        print("Meeting email failed:", e)

    return {
        "id": schedule.id,
        "title": consultation.topic,
        "date": scheduled_time.date().isoformat(),
        "time": scheduled_time.strftime("%H:%M"),
        "platform": "teams" if "teams" in (meeting_link or "").lower() else "google",
        "participants": consultation.user_email,
        "meeting_link": meeting_link
    }


# ---------------------------------------------------------
# Get all scheduled consultations (dashboard)
# ---------------------------------------------------------
@router.get("/scheduled")
def get_all_scheduled(db: Session = Depends(get_db)):
    schedules = db.query(ConsultationSchedule).all()
    result = []

    for s in schedules:
        consultation = db.query(Consultation).filter(Consultation.id == s.consultation_id).first()

        result.append({
            "id": s.id,
            "title": consultation.topic,
            "date": s.scheduled_time.date().isoformat(),
            "time": s.scheduled_time.strftime("%H:%M"),
            "platform": "teams" if "teams" in (s.meeting_link or "").lower() else "google",
            "participants": consultation.user_email,
            "meeting_link": s.meeting_link
        })

    return result
