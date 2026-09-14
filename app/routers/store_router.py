from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.products import Product

# ⭐ THIS MUST EXIST — otherwise main.py cannot import router
router = APIRouter(prefix="/store", tags=["Store"])


# ---------------------------------------------------------
# GET ALL PRODUCTS
# ---------------------------------------------------------
@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return [
        {
            "item_id": p.item_id,
            "name": p.name,
            "type": p.type,
            "price_usd": p.price_usd,
            "billing_period": p.billing_period,
            "active": p.active,
            "coming_soon": p.coming_soon,
            "description": p.description,
        }
        for p in products
    ]


# ---------------------------------------------------------
# GET SINGLE PRODUCT
# ---------------------------------------------------------
@router.get("/product/{item_id}")
def get_product(item_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.item_id == item_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "item_id": product.item_id,
        "name": product.name,
        "type": product.type,
        "price_usd": product.price_usd,
        "billing_period": product.billing_period,
        "active": product.active,
        "coming_soon": product.coming_soon,
        "description": product.description,
    }
