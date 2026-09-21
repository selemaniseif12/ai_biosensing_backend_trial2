from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db

from app.services.ml_admin_service import service_list_ml_logs

router = APIRouter(
    prefix="/ml-admin",
    tags=["ML Admin"]
)

@router.get("/logs")
def list_ml_logs(db: Session = Depends(get_db)):
    return service_list_ml_logs(db)
