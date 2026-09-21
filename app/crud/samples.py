from sqlalchemy.orm import Session
from app.schemas.samples import SampleCreate

from app.models.sample import Sample  # ⭐ THIS WAS MISSING

def get_samples(db: Session):
    return db.query(Sample).all()

def get_sample(db: Session, sample_id: int):
    return db.query(Sample).filter(Sample.id == sample_id).first()

def create_sample(db: Session, sample: SampleCreate):
    db_sample = Sample(
        sample_name=sample.sample_name,
        description=sample.description,
        customer_id=sample.customer_id
    )
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample
