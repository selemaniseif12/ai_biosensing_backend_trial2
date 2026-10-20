from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.cart_item import CartItem
from app.models.products import Product
from app.models.user import User


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


class CartAddRequest(BaseModel):
    item_id: str


# ---------------------------------------------------------
# GET THE AUTHENTICATED CUSTOMER'S CART
# ---------------------------------------------------------

@router.get("")
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .all()
    )


# ---------------------------------------------------------
# ADD A PRODUCT TO THE AUTHENTICATED CUSTOMER'S CART
# ---------------------------------------------------------

@router.post("/add")
def add_to_cart(
    payload: CartAddRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item_id = payload.item_id.strip()

    if not item_id:
        raise HTTPException(
            status_code=400,
            detail="A valid product ID is required.",
        )

    # Always retrieve product details from the database.
    product = (
        db.query(Product)
        .filter(Product.item_id == item_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Store item not found.",
        )

    # Only search the authenticated customer's cart.
    existing = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.item_id == product.item_id,
        )
        .first()
    )

    if existing:
        existing.quantity += 1
        existing.item_name = product.name
        existing.price_usd = product.price_usd

        try:
            db.commit()
            db.refresh(existing)
        except Exception:
            db.rollback()
            raise

        return {
            "message": "Quantity updated.",
            "item": {
                "item_id": existing.item_id,
                "item_name": existing.item_name,
                "quantity": existing.quantity,
                "price_usd": existing.price_usd,
            },
        }

    cart_item = CartItem(
        user_id=current_user.id,
        item_id=product.item_id,
        item_name=product.name,
        quantity=1,
        price_usd=product.price_usd,
    )

    try:
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Added to cart.",
        "item": {
            "item_id": cart_item.item_id,
            "item_name": cart_item.item_name,
            "quantity": cart_item.quantity,
            "price_usd": cart_item.price_usd,
        },
    }


# ---------------------------------------------------------
# DELETE FROM THE AUTHENTICATED CUSTOMER'S CART
# ---------------------------------------------------------

@router.delete("/delete")
def delete_cart_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item_id = item_id.strip()

    if not item_id:
        raise HTTPException(
            status_code=400,
            detail="A valid product ID is required.",
        )

    item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.item_id == item_id,
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found in your cart.",
        )

    try:
        db.delete(item)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Item deleted.",
        "item_id": item_id,
    }