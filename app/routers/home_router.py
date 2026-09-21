from fastapi import APIRouter

router = APIRouter(prefix="/home", tags=["Home"])

@router.get("/")
def home():
    return {
        "title": "AI Biosensing & Data Analytics Consulting",
        "description": "Full‑stack API development, biosensing analytics, and ML‑powered detection demos.",
        "links": {
            "api_docs": "/docs",
            "devices": "/devices",
            "viruses": "/viruses",
            "detection_demo": "/detect"
        }
    }
