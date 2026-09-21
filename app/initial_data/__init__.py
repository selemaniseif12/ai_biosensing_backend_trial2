from sqlalchemy.orm import Session
from app.initial_data.load_documents import load_initial_documents

def run_initial_load(db: Session):
    """
    Runs all initial data loaders (currently: documentation metadata).
    """
    load_initial_documents(db)
