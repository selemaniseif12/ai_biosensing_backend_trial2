from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Database dependency
from app.dependencies.db import get_db

# Models
from app.models.virus import Virus
from app.models.detection import Detection

# Schemas
from app.schemas.detection_schemas import DetectionRequest, DetectionResponse

# Services (physics + ML)
from app.services.detection_service import (
    physics_estimate,
    simple_ml_time_to_detection,
    simple_ml_confidence
)

router = APIRouter(prefix="/detect", tags=["Detection"])


# ---------------------------------------------------------
# CREATE DETECTION
# ---------------------------------------------------------
@router.post("/", response_model=DetectionResponse)
def detect(request: DetectionRequest, db: Session = Depends(get_db)):

    virus = db.query(Virus).filter(Virus.id == request.virus_id).first()
    if not virus:
        raise HTTPException(status_code=404, detail="Virus not found")

    # Physics model
    physics_count = physics_estimate(
        mass_fg=virus.mass_fg,
        mass_per_virus_fg=virus.mass_fg
    )

    physics_mass_change = virus.mass_fg

    # ML model
    ml_time = simple_ml_time_to_detection(
        request.deposition_rate,
        request.temperature,
        request.humidity,
        request.flow_rate
    )

    ml_conf = simple_ml_confidence()

    # Save detection
    detection = Detection(
        virus_id=virus.id,
        device_id=request.device_id,
        physics_estimated_count=physics_count,
        physics_mass_change_fg=physics_mass_change,
        ml_estimated_time_to_detection=ml_time,
        ml_confidence=ml_conf
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)

    return DetectionResponse(
        virus=virus.name,
        device_id=request.device_id,
        physics_estimated_count=physics_count,
        physics_mass_change_fg=physics_mass_change,
        ml_estimated_time_to_detection=ml_time,
        ml_confidence=ml_conf
    )


# ---------------------------------------------------------
# GET ALL DETECTIONS
# ---------------------------------------------------------
@router.get("/history")
def get_detection_history(db: Session = Depends(get_db)):
    return db.query(Detection).order_by(Detection.created_at.desc()).all()


# ---------------------------------------------------------
# GET DETECTION BY ID
# ---------------------------------------------------------
@router.get("/{detection_id}")
def get_detection_by_id(detection_id: int, db: Session = Depends(get_db)):
    det = db.query(Detection).filter(Detection.id == detection_id).first()
    if not det:
        raise HTTPException(status_code=404, detail="Detection not found")
    return det


# ---------------------------------------------------------
# GET DETECTIONS FOR DEVICE
# ---------------------------------------------------------
@router.get("/device/{device_id}")
def get_detection_for_device(device_id: int, db: Session = Depends(get_db)):
    return db.query(Detection).filter(Detection.device_id == device_id).all()


# ---------------------------------------------------------
# GET DETECTIONS FOR VIRUS
# ---------------------------------------------------------
@router.get("/virus/{virus_id}")
def get_detection_for_virus(virus_id: int, db: Session = Depends(get_db)):
    return db.query(Detection).filter(Detection.virus_id == virus_id).all()


# ---------------------------------------------------------
# DETECTION STATISTICS
# ---------------------------------------------------------
@router.get("/stats")
def get_detection_stats(db: Session = Depends(get_db)):
    total = db.query(Detection).count()

    virus_counts = {}
    viruses = db.query(Virus).all()
    for v in viruses:
        count = db.query(Detection).filter(Detection.virus_id == v.id).count()
        virus_counts[v.name] = count

    conf_values = db.query(Detection.ml_confidence).all()
    avg_conf = sum([c[0] for c in conf_values]) / len(conf_values) if conf_values else 0

    return {
        "total_detections": total,
        "detections_per_virus": virus_counts,
        "average_confidence": round(avg_conf, 3)
    }
