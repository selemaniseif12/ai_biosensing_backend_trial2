# app/seed/store_seed.py

from sqlalchemy.orm import Session
from app.models.products import Product   # ✅ Correct import

# Combined product list (your original + new verified items)
PRODUCTS = [
    {
        "item_id": "consulting_fixed",
        "name": "Fixed Consulting Package",
        "type": "service",
        "price_usd": 199.00,
        "billing_period": "one_time",
        "description": "One-hour consulting session for biosensing or ML guidance",
    },
    {
        "item_id": "consulting_custom",
        "name": "Custom Consulting Package",
        "type": "service",
        "price_usd": 499.00,
        "billing_period": "one_time",
        "description": "Custom project consulting for labs, research teams, or startups",
    },
    {
        "item_id": "course_intro",
        "name": "Intro to Biosensing & Frequency Noise",
        "type": "course",
        "price_usd": 59.00,
        "billing_period": "3_months",
        "description": "Foundational course on QCM sensors, noise, and biosensing basics",
    },
    {
        "item_id": "course_ml_v2",
        "name": "ML V2 Training Course",
        "type": "course",
        "price_usd": 79.00,
        "billing_period": "3_months",
        "description": "Training on XGBoost V2 model, noise tables, and lab workflow",
    },
    {
        "item_id": "course_ml_v6",
        "name": "ML V6 Training Course",
        "type": "course",
        "price_usd": 99.00,
        "billing_period": "3_months",
        "description": "Advanced RandomForest V6 training with 120k dataset",
    },
    {
        "item_id": "course_fullstack_api",
        "name": "Full Stack API Engineering Course",
        "type": "course",
        "price_usd": 799.00,
        "billing_period": "3_months",
        "description": "End-to-end API engineering, backend, routers, models, and dashboards",
    },
    {
        "item_id": "ml_v2",
        "name": "ML V2 Model Access",
        "type": "digital",
        "price_usd": 49.00,
        "billing_period": "3_months",
        "description": "Access to Analyzer V2 model, logs, noise tables, and predictions",
    },
    {
        "item_id": "ml_v6",
        "name": "ML V6 Model Access",
        "type": "digital",
        "price_usd": 69.00,
        "billing_period": "3_months",
        "description": "Access to Analyzer V6 model, logs, noise tables, and predictions",
    },
    {
        "item_id": "ml_bundle_v2_v6",
        "name": "ML V2/V6 Bundle",
        "type": "digital",
        "price_usd": 99.00,
        "billing_period": "3_months",
        "description": "Combined access to both ML models with comparison dashboard",
    },
    {
        "item_id": "virus_list",
        "name": "Virus Database Subscription",
        "type": "digital",
        "price_usd": 29.00,
        "billing_period": "3_months",
        "description": "Access to 100-virus database with mass, metadata, and probabilities",
    },
    {
        "item_id": "device_lowgrade",
        "name": "Low-Grade Patented Biosensing Device",
        "type": "physical",
        "price_usd": 299.00,
        "billing_period": "one_time",
        "description": "Educational QCM device for practical biosensing experiments",
    },
]


def seed_store_products(db: Session):
    for p in PRODUCTS:
        # Avoid duplicates
        exists = db.query(Product).filter(Product.item_id == p["item_id"]).first()
        if exists:
            continue

        product = Product(
            item_id=p["item_id"],
            name=p["name"],
            type=p["type"],
            price_usd=p["price_usd"],
            billing_period=p["billing_period"],
            description=p["description"],
        )

        db.add(product)

    db.commit()
    print("Store products seeded successfully.")
