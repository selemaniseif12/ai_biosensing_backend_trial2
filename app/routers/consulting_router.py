from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.consulting_model import ConsultingRequestModel

# ⭐ RATE LIMIT & LOGGER REMOVED
# from app.services.rate_limit import rate_limit
# from app.services.usage_logger import log_usage

from app.utils.email_sender import send_email   # <-- Correct Gmail SMTP sender

router = APIRouter(prefix="/consulting", tags=["Consulting"])


class ConsultingRequest(BaseModel):
    name: str
    email: str
    organization: str | None = None
    api_key: str | None = None
    project_description: str
    services: list[str]


def save_request_to_db(payload: ConsultingRequest):
    try:
        db: Session = SessionLocal()
        entry = ConsultingRequestModel(
            name=payload.name,
            email=payload.email,
            organization=payload.organization,
            api_key=payload.api_key,
            project_description=payload.project_description,
            services=",".join(payload.services)
        )
        db.add(entry)
        db.commit()
        db.close()
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database insert failed.")


def notify_selemani(payload: ConsultingRequest):
    # ⭐ ADMIN EMAIL (to you)
    admin_body = (
        f"New consulting request received.\n\n"
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n"
        f"Organization: {payload.organization}\n"
        f"API Key: {payload.api_key}\n"
        f"Project Description:\n{payload.project_description}\n\n"
        f"Requested Services: {', '.join(payload.services)}"
    )

    send_email(
        to_email="selemaniseif12@yahoo.com",   # FIXED
        subject="New Consulting Request",
        body=admin_body
    )

    # ⭐ USER CONFIRMATION EMAIL
    user_body = (
        f"Hello {payload.name},\n\n"
        f"Thank you for your consulting request.\n"
        f"We have received your project details and will contact you soon.\n\n"
        f"Your submitted services: {', '.join(payload.services)}\n\n"
        f"Best regards,\nAI Biosensing Team"
    )

    send_email(
        to_email=payload.email,               # FIXED
        subject="Your Consulting Request Has Been Received",
        body=user_body
    )


@router.post("")
def submit_consulting_request(payload: ConsultingRequest):
    """
    Submit a consulting request.
    - Rate limiting disabled
    - Usage logging disabled
    """

    # ⭐ RATE LIMITING DISABLED
    # rate_limit("public", endpoint="consulting_submit")

    # ⭐ USAGE LOGGING DISABLED
    # log_usage(
    #     token="public",
    #     endpoint="consulting_submit",
    #     details=f"Consulting request from {payload.email}"
    # )

    save_request_to_db(payload)
    notify_selemani(payload)

    return {
        "message": "Your consulting request was delivered successfully and logged."
    }
