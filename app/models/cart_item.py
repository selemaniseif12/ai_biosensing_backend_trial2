from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    # ⭐ FIXED: item_id must be INTEGER to match Product.item_id
    item_id = Column(Integer, index=True)

    item_name = Column(String)
    price_usd = Column(Float)
    quantity = Column(Integer)
