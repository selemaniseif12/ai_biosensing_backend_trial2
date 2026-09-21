from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db

from app.models.detection import Detection
from app.models.virus import Virus

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/virus-counts")
def virus_counts(db: Session = Depends(get_db)):
    results = db.query(
        Virus.name,
        Detection.device_id,
    ).join(Detection, Virus.id == Detection.virus_id).all()

    return {"counts": results}
