from sqlalchemy.orm import Session
from app.models.ml_log import MLLog

# ---------------------------------------------------------
# ML LOG CRUD
# ---------------------------------------------------------

def get_logs(db: Session):
    """Retrieve all ML logs."""
    return db.query(MLLog).all()


def get_log(db: Session, log_id: int):
    """Retrieve a single ML log by ID."""
    return db.query(MLLog).filter(MLLog.id == log_id).first()


def create_log(db: Session, model_name: str, version: str, status: str, message: str = None):
    """Create a new ML log entry."""
    log = MLLog(
        model_name=model_name,
        version=version,
        status=status,
        message=message,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def delete_log(db: Session, log_id: int):
    """Delete an ML log entry by ID."""
    log = get_log(db, log_id)
    if not log:
        return False

    db.delete(log)
    db.commit()
    return True


# ---------------------------------------------------------
# USAGE LOG ALIASES
# ---------------------------------------------------------

def get_usage_log(db: Session):
    """Retrieve all usage logs (alias for ML logs)."""
    return db.query(MLLog).all()


def create_usage_log(db: Session, model_name: str, version: str, status: str, message: str = None):
    """Create a usage log entry (alias for ML log creation)."""
    return create_log(db, model_name, version, status, message)


def delete_usage_log(db: Session, log_id: int):
    """Delete a usage log entry (alias for ML log deletion)."""
    return delete_log(db, log_id)


# Backward compatibility aliases
get_usage_logs = get_usage_log
