from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.cart_item import CartItem

# ✅ Correct model import
from app.models.products import Product

router = APIRouter(prefix="/store/cart", tags=["Cart"])

class CartAddRequest(BaseModel):
    item_id: str


# ---------------------------
# GET CART ITEMS
# ---------------------------
@router.get("")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


# ---------------------------
# ADD ITEM TO CART
# ---------------------------
@router.post("/add")
def add_to_cart(user_id: int, payload: CartAddRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.item_id == payload.item_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Store item not found")

    # ⭐ If item already exists, increase quantity instead of inserting duplicate
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.item_id == payload.item_id
    ).first()

    if existing:
        existing.quantity += 1
        db.commit()
        db.refresh(existing)
        return {
            "message": "Quantity updated",
            "item": {
                "item_id": existing.item_id,
                "item_name": existing.item_name,
                "quantity": existing.quantity,
                "price_usd": existing.price_usd
            }
        }

    # Create new cart item
    cart_item = CartItem(
        user_id=user_id,
        item_id=product.item_id,
        item_name=product.name,
        quantity=1,
        price_usd=product.price_usd
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Added to cart",
        "item": {
            "item_id": cart_item.item_id,
            "item_name": cart_item.item_name,
            "quantity": cart_item.quantity,
            "price_usd": cart_item.price_usd
        }
    }


# ---------------------------
# DELETE ITEM FROM CART
# ---------------------------
@router.delete("/delete")
def delete_cart_item(user_id: int, item_id: str, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.item_id == item_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}


# ---------------------------
# ALIAS ROUTES
# ---------------------------
alias_router = APIRouter(tags=["Cart Alias"])

@alias_router.post("/cart/add")
def alias_add_to_cart(user_id: int, payload: CartAddRequest, db: Session = Depends(get_db)):
    return add_to_cart(user_id=user_id, payload=payload, db=db)

@alias_router.get("/cart")
def alias_get_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart(user_id=user_id, db=db)

@alias_router.delete("/cart/delete")
def alias_delete_cart_item(user_id: int, item_id: str, db: Session = Depends(get_db)):
    return delete_cart_item(user_id=user_id, item_id=item_id, db=db)
