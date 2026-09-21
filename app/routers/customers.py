# ============================================================
# File: routers/customers.py
# Description: FastAPI router for customer retrieval endpoints.
# Author: Selemani
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Use your REAL database system
from app.dependencies.db import get_db


# ✅ Correct Customer model import (from app/models/, NOT db_models)
from app.models.customer import Customer

router = APIRouter()

@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    """
    Returns all customers from the database.
    No query parameters required.
    """
    return db.query(Customer).all()
