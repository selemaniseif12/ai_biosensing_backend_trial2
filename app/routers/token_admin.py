import hmac

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.token_model import TokenModel


def require_root_admin_key(
    x_root_admin_key: str | None = Header(default=None, alias="X-Root-Admin-Key"),
):
    """Reject requests unless a valid root admin key is configured and supplied."""
    configured_key = settings.ROOT_ADMIN_API_KEY

    if (
        not configured_key
        or configured_key == "CHANGE_ME_ADMIN_KEY"
        or not x_root_admin_key
        or not hmac.compare_digest(x_root_admin_key, configured_key)
    ):
        raise HTTPException(
            status_code=403,
            detail="Root admin authorization required",
        )


router = APIRouter(
    prefix="/admin/tokens",
    tags=["Admin Token Control"],
    dependencies=[Depends(require_root_admin_key)],
)


@router.get("/list")
def list_tokens(db: Session = Depends(get_db)):
    """List all tokens."""
    tokens = db.query(TokenModel).all()
    return tokens


@router.post("/create")
def create_token(
    service_name: str,
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    """Manually create a new token."""
    token_obj = TokenModel.create_token(
        db=db,
        token_type=service_name,
        user_id=user_id,
        description=f"Admin-created token for {service_name}",
    )
    return {
        "status": "created",
        "token": token_obj.token,
        "service": service_name,
        "user_id": user_id,
    }


@router.post("/disable/{token}")
def disable_token(token: str, db: Session = Depends(get_db)):
    """Disable an existing token."""
    token_obj = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    token_obj.is_active = False
    db.commit()

    return {"status": "disabled", "token": token}


@router.post("/activate/{token}")
def activate_token(token: str, db: Session = Depends(get_db)):
    """Re-activate a disabled token."""
    token_obj = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    token_obj.is_active = True
    db.commit()

    return {"status": "activated", "token": token}


@router.post("/extend/{token}")
def extend_token_expiration(
    token: str,
    days: int = 30,
    db: Session = Depends(get_db),
):
    """Extend token expiration."""
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=400,
            detail="Days must be between 1 and 365",
        )

    token_obj = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    from datetime import datetime, timedelta

    token_obj.expires_at = datetime.utcnow() + timedelta(days=days)
    db.commit()

    return {
        "status": "extended",
        "token": token,
        "new_expiration": token_obj.expires_at,
    }
