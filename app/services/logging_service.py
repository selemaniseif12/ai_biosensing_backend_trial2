from sqlalchemy.orm import Session
from app.models.models import AnalysisLog


def log_analysis(db: Session, version: str, features: list, prediction: int, confidence: float):
    """
    Store an analysis event in the database for analytics, dashboards, and auditing.
    """
    entry = AnalysisLog(
        version=version,
        features=features,
        prediction=prediction,
        confidence=confidence
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry
