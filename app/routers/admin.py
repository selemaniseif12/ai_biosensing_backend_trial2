from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.crud.api_keys import (
    create_api_key,
    list_api_keys_for_customer,
    get_api_key_by_value,
    revoke_api_key,
    activate_api_key,
    rotate_api_key,
)
from app.routers.customers import get_customer


router = APIRouter(
    prefix="/admin",
    tags=["Admin API Keys"]
)


# ---------------------------------------------------------
# List all API keys for a customer
# ---------------------------------------------------------
@router.get("/customers/{customer_id}/api-keys")
def admin_list_api_keys(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    keys = list_api_keys_for_customer(db, customer_id)

    return [
        {
            "id": k.id,
            "key": k.key,
            "name": k.name,
            "active": k.active,
            "total_calls": k.total_calls,
            "monthly_limit": k.monthly_limit,
            "created_at": k.created_at,
            "revoked_at": k.revoked_at,
        }
        for k in keys
    ]


# ---------------------------------------------------------
# Create API key for a customer
# ---------------------------------------------------------
@router.post("/customers/{customer_id}/api-keys")
def admin_create_api_key(
    customer_id: int,
    name: str | None = None,
    monthly_limit: int = 0,
    db: Session = Depends(get_db),
):
    customer = get_customer(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    key = create_api_key(db, customer_id, name=name, monthly_limit=monthly_limit)

    return {
        "id": key.id,
        "key": key.key,
        "name": key.name,
        "active": key.active,
        "monthly_limit": key.monthly_limit,
        "created_at": key.created_at,
        "revoked_at": key.revoked_at,
    }
