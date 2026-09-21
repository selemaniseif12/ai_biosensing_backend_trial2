from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.token_model import ServiceToken


def verify_token(token: str, service_name: str, db: Session = Depends(get_db)):
    """
    Verifies that:
    - The token exists
    - The token is active
    - The token matches the requested service
    """

    record = (
        db.query(ServiceToken)
        .filter(ServiceToken.token == token)
        .filter(ServiceToken.service_name == service_name)
        .filter(ServiceToken.is_active == True)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Invalid or inactive token for this service"
        )

    return record
