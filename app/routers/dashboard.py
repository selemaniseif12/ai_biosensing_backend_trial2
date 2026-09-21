# ============================================================
# File: routers/dashboard.py
# Description: FastAPI router for dashboard summary endpoints.
# Author: Selemani
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.customer import Customer
from app.models.virus import Virus

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return {
        "total_customers": db.query(Customer).count(),
        "total_viruses": db.query(Virus).count(),
    }
