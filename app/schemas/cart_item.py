from pydantic import BaseModel, ConfigDict

class CartItem(BaseModel):
    id: int
    user_id: int
    item_id: str
    item_name: str
    item_type: str
    price_usd: float
    quantity: int

    # ⭐ REQUIRED for SQLAlchemy → Pydantic conversion
    model_config = ConfigDict(from_attributes=True)


class CartItemCreate(BaseModel):
    user_id: int
    item_id: str
    quantity: int
