from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db

from app.schemas.samples import SampleCreate, SampleUpdate
from app.services.sample_service import (
    create_sample,
    get_sample,
    get_all_samples,
    update_sample,
    delete_sample,
)

router = APIRouter(tags=["Samples"])


@router.post("/")
def create(sample: SampleCreate, db: Session = Depends(get_db)):
    return create_sample(sample, db)


@router.get("/{sample_id}")
def read(sample_id: int, db: Session = Depends(get_db)):
    sample = get_sample(sample_id, db)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    return get_all_samples(db)


@router.put("/{sample_id}")
def update(sample_id: int, sample: SampleUpdate, db: Session = Depends(get_db)):
    updated = update_sample(sample_id, sample, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Sample not found")
    return updated


@router.delete("/{sample_id}")
def delete(sample_id: int, db: Session = Depends(get_db)):
    deleted = delete_sample(sample_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sample not found")
    return {"deleted": True}
