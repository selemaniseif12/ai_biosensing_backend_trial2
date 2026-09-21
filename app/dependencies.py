from sqlalchemy.orm import Session
from app.database import SessionLocal

# ---------------------------------------------------------
# Database Session Dependency
# ---------------------------------------------------------
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
