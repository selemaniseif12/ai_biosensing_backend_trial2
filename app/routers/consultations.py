from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consultations import Consultation

router = APIRouter()

@router.post("/consultations/{consultation_id}/schedule")
def schedule_consultation(
    consultation_id: int,
    scheduled_time: str,
    meeting_link: str = None,
    db: Session = Depends(get_db)
):
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consultation.scheduled_time = scheduled_time
    consultation.meeting_link = meeting_link
    consultation.status = "scheduled"

    db.commit()
    db.refresh(consultation)

    return {
        "id": consultation.id,
        "consultation_id": consultation.id,
        "scheduled_time": consultation.scheduled_time,
        "meeting_link": consultation.meeting_link,
        "status": consultation.status
    }
