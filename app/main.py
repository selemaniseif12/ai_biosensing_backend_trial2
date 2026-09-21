from dotenv import load_dotenv
load_dotenv()

import os
import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.core.logging_config import LOGGING_CONFIG
from app.database import Base, engine, SessionLocal, init_db

# MODELS REQUIRED FOR ACTIVE ROUTERS
from app.models.consultations import Consultation
from app.models.consulting_model import ConsultingRequestModel
from app.models.token_model import TokenModel
from app.models.user import User

# ---------------------------
# ACTIVE ROUTERS (Layer 1 + Layer 2 + Simple Admin + Virus List)
# ---------------------------

# Public
from app.routers.home_router import router as home_router
from app.routers.profile_router import router as profile_router
from app.routers.docs import router as docs_router

# Auth
from app.routers.auth import router as auth_router

# Consulting (public + admin)
from app.routers.consultations import router as consultations_router
from app.routers.consulting_router import router as consulting_router

# Admin (simple)
from app.routers.token_admin import router as token_admin_router
from app.routers.consultation_schedule_router import router as consultation_schedule_router

# Virus List (ACTIVE)
from app.routers.virus_list import router as virus_list_router

# ML (public + user)
from app.routers.sensor_live_drift import router as sensor_live_drift_router
from app.routers.ml_training_router import router as ml_training_router

# ---------------------------
# COMMENTED OUT — NOT IN FINAL RELEASE
# ---------------------------

# from app.routers.calendar_router import router as calendar_router   # ❌ REMOVED — BROKEN
# from app.routers.notification_router import router as notification_router
# from app.routers.team_workload_router import router as team_workload_router
# from app.routers.students import router as students_router
# from app.routers.store_router import router as store_router
# from app.routers.cart_router import router as cart_router
# from app.routers.checkout_router import router as checkout_router
# from app.routers.payment_webhook import router as payment_webhook_router
# from app.routers.payments_router import router as payments_router
# from app.routers.stripe_router import router as stripe_router
# from app.routers.webhook import router as stripe_webhook_router
# from app.routers.course_router import router as course_router
# from app.routers.course_module_router import router as course_module_router
# from app.routers.course_content_router import router as course_content_router
# from app.routers.course_access_router import router as course_access_router
# from app.routers.enrollment import router as enrollment_router
# from app.routers.activity import router as activity_router
# from app.routers.receipts_router import init_receipts

# ---------------------------
# Lifespan
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="AI Biosensing API",
    version="1.0.0",
    description="Copyright © 2026 Piezo Pico to Femtotechnology Sensors Inc.",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-biosensing-frontend-v2.vercel.app",
        "https://api.piezo-sensors.com",
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup
@app.on_event("startup")
async def startup_event():
    logging.config.dictConfig(LOGGING_CONFIG)
    init_db()

# Static files
os.makedirs("static/slides", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Docs content
app.mount("/docs_content", StaticFiles(directory="app/docs_content"), name="docs_content")

# ---------------------------
# ACTIVE ROUTERS (FINAL RELEASE)
# ---------------------------

# Auth
app.include_router(auth_router, tags=["Auth"])

# Public
app.include_router(home_router, tags=["Home"])
app.include_router(profile_router, prefix="/app", tags=["Profile"])
app.include_router(docs_router, tags=["Documents"])

# Consulting (public + admin)
app.include_router(consultations_router, tags=["Consultations"])
app.include_router(consulting_router)

# Admin (simple)
app.include_router(token_admin_router)
app.include_router(consultation_schedule_router)

# Virus List
app.include_router(virus_list_router, tags=["Virus List"])

# ML (public + user)
app.include_router(ml_training_router, tags=["ML Training"])
app.include_router(sensor_live_drift_router)

# ---------------------------
# Email sender
# ---------------------------
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

class EmailRequest(BaseModel):
    to: str
    subject: str
    message: str

@app.post("/send-email")
def send_email(req: EmailRequest):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = req.subject
    msg["From"] = EMAIL_USER
    msg["To"] = req.to

    html = f"""
    <html>
      <body>
        <h2>{req.subject}</h2>
        <p>{req.message}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(req.message, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())

        return {"status": "sent", "to": req.to}

    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/")
def root():
    return {"message": "AI Biosensing API is running"}

# Render server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
