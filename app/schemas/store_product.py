# app/schemas/store_product.py

from pydantic import BaseModel

class StoreProductBase(BaseModel):
    item_id: str
    name: str
    type: str
    price_usd: float
    billing_period: str
    description: str | None = None

class StoreProductCreate(StoreProductBase):
    pass

class StoreProduct(StoreProductBase):
    id: int

    class Config:
        orm_mode = True
