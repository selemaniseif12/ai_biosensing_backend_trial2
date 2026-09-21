from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.api_key_service import validate_api_key


def require_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    customer = validate_api_key(db, x_api_key)
    if not customer:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return customer
