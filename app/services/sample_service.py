from sqlalchemy.orm import Session
from app.models.models import Sample


def create_sample(sample_data, db: Session):
    sample = Sample(
        customer_id=sample_data.customer_id,
        description=sample_data.description,
    )
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


def get_sample(sample_id: int, db: Session):
    return db.query(Sample).filter(Sample.id == sample_id).first()


def get_all_samples(db: Session):
    return db.query(Sample).all()


def update_sample(sample_id: int, sample_data, db: Session):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        return None

    sample.customer_id = sample_data.customer_id
    sample.description = sample_data.description

    db.commit()
    db.refresh(sample)
    return sample


def delete_sample(sample_id: int, db: Session):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        return None

    db.delete(sample)
    db.commit()
    return {"deleted": True}
