from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    # item_id MUST match Product.item_id (String)
    item_id = Column(String(100), index=True)

    item_name = Column(String)
    price_usd = Column(Float)
    quantity = Column(Integer)
