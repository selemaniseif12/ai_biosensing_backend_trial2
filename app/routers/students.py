from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.students import Student

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


