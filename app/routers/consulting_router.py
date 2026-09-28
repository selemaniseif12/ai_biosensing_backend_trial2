from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.consulting_model import ConsultingRequestModel

# ⭐ NEW IMPORTS
from app.services.rate_limit import rate_limit
from app.services.usage_logger import log_usage

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
    print("CONSULTING REQUEST RECEIVED:")
    print(payload.dict())
    # Render-safe: no SMTP


@router.post("")
def submit_consulting_request(payload: ConsultingRequest, token: str):
    """
    Submit a consulting request.
    - Rate-limited
    - Usage logged
    """

    # ⭐ RATE LIMITING
    rate_limit(token, endpoint="consulting_submit")

    # ⭐ USAGE LOGGING
    log_usage(
        token=token,
        endpoint="consulting_submit",
        details=f"Consulting request from {payload.email}"
    )

    print("Received consulting request:", payload.dict())

    save_request_to_db(payload)
    notify_selemani(payload)

    return {
        "message": "Your consulting request was delivered successfully and logged."
    }
