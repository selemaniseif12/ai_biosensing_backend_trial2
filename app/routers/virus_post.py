# app/routers/virus_post.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.database import Base, engine, SessionLocal

from app.models.virus import Virus


router = APIRouter(prefix="/virus", tags=["Virus"])

class VirusCreate(BaseModel):
    name: str
    family: str | None = None
    description: str | None = None

@router.post("/")
def create_virus(virus: VirusCreate):
    db = SessionLocal()
    try:
        new_virus = Virus(
            name=virus.name,
            family=virus.family,
            description=virus.description,
        )
        db.add(new_virus)
        db.commit()
        db.refresh(new_virus)
        return {
            "message": "Virus added successfully",
            "virus": {
                "id": new_virus.id,
                "name": new_virus.name,
                "family": new_virus.family,
                "description": new_virus.description,
            },
        }
    finally:
        db.close()
