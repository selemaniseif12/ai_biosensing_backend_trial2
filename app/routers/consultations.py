from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.consultations import Consultation

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage
from app.services.email_service import send_email   # <-- Gmail SMTP sender

router = APIRouter(prefix="/consultations", tags=["Consultation Management"])


# ---------------------------------------------------------
# Helper: Convert ORM → JSON-safe dict
# ---------------------------------------------------------
def consultation_to_dict(c: Consultation):
    return {
        "id": c.id,
        "consultation_id": c.id,
        "scheduled_time": (
            c.scheduled_time.isoformat() if isinstance(c.scheduled_time, datetime) else c.scheduled_time
        ),
        "meeting_link": c.meeting_link,
        "status": c.status
    }


# ---------------------------------------------------------
# Schedule a consultation
# ---------------------------------------------------------
@router.post("/{consultation_id}/schedule")
def schedule_consultation(
    consultation_id: int,
    scheduled_time: str,
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
    rate_limit(token, endpoint="consultation_schedule")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="consultation_schedule",
        details=f"Scheduled consultation {consultation_id}"
    )

    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    # Convert incoming string → datetime
    try:
        parsed_time = datetime.fromisoformat(scheduled_time)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")

    # Update consultation
    consultation.scheduled_time = parsed_time
    consultation.meeting_link = meeting_link
    consultation.status = "scheduled"

    db.commit()
    db.refresh(consultation)

    # ⭐ EMAIL NOTIFICATIONS (Gmail SMTP)
    user_email = getattr(consultation, "user_email", None)

    # Send confirmation to user
    if user_email:
        send_email(
            email_to=user_email,
            subject="Your Consultation Has Been Scheduled",
            body=(
                f"Hello,\n\n"
                f"Your consultation has been scheduled.\n\n"
                f"Date: {parsed_time.date().isoformat()}\n"
                f"Time: {parsed_time.strftime('%H:%M')}\n"
                f"Meeting Link: {meeting_link}\n\n"
                f"Thank you."
            )
        )

    # Send admin notification
    send_email(
        email_to="selemaniseif12@yahoo.com",
        subject="New Consultation Scheduled",
        body=(
            f"A consultation has been scheduled.\n\n"
            f"Consultation ID: {consultation.id}\n"
            f"User Email: {user_email}\n"
            f"Date: {parsed_time.date().isoformat()}\n"
            f"Time: {parsed_time.strftime('%H:%M')}\n"
            f"Meeting Link: {meeting_link}\n"
        )
    )

    return consultation_to_dict(consultation)
