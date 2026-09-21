from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.database import SessionLocal
from app.models.module import Module

router = APIRouter()

# ---------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------
class ModuleCreate(BaseModel):
    module_id: int
    module_title: str
    description: str

class BulkModuleCreate(BaseModel):
    modules: List[ModuleCreate]


# ---------------------------------------------------------
# POST /modules/bulk  → Create multiple modules
# ---------------------------------------------------------
@router.post("/modules/bulk")
def create_modules_bulk(payload: BulkModuleCreate):
    db = SessionLocal()
    created = []
    skipped = []

    try:
        for m in payload.modules:
            existing = db.query(Module).filter_by(module_id=m.module_id).first()
            if existing:
                skipped.append({
                    "module_id": m.module_id,
                    "reason": "Module already exists"
                })
                continue

            new_module = Module(
                module_id=m.module_id,
                module_title=m.module_title,
                description=m.description
            )
            db.add(new_module)
            created.append({
                "module_id": m.module_id,
                "status": "created"
            })

        db.commit()

        return {
            "created": created,
            "skipped": skipped,
            "total_created": len(created),
            "total_skipped": len(skipped)
        }

    finally:
        db.close()


# ---------------------------------------------------------
# GET /modules  → Return all modules
# ---------------------------------------------------------
@router.get("/modules")
def get_all_modules():
    db = SessionLocal()
    try:
        modules = db.query(Module).all()
        return modules
    finally:
        db.close()


# ---------------------------------------------------------
# GET /modules/{module_id}  → Return one module
# ---------------------------------------------------------
@router.get("/modules/{module_id}")
def get_module(module_id: int):
    db = SessionLocal()
    try:
        module = db.query(Module).filter_by(module_id=module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        return module
    finally:
        db.close()
