from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import math

from app.dependencies.db import get_db
from app.models.virus import Virus


router = APIRouter(prefix="/probability", tags=["Virus Probability"])

class ProbabilityInput(BaseModel):
    virus_id: int
    particle_count: float

@router.post("/detect")
def detection_probability(data: ProbabilityInput, db: Session = Depends(get_db)):

    virus = db.query(Virus).filter(Virus.id == data.virus_id).first()
    if not virus:
        raise HTTPException(status_code=404, detail="Virus not found")

    # logistic model
    x = data.particle_count / virus.sensitivity_fg
    probability = 1 / (1 + math.exp(-x))

    return {
        "virus": virus.name,
        "particle_count": data.particle_count,
        "probability": probability
    }
