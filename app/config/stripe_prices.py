# app/config/stripe_prices.py

STRIPE_PRICES = {
    # -----------------------------
    # COURSE OUTLINES (disabled)
    # -----------------------------
    "course_intro": "price_xxx_intro",
    "course_ml_v2": "price_xxx_course_ml_v2",
    "course_ml_v6": "price_xxx_course_ml_v6",

    # -----------------------------
    # ML MODELS (enabled)
    # -----------------------------
    "ml_v2": "price_xxx_ml_v2",
    "ml_v6": "price_xxx_ml_v6",
    "ml_bundle_v2_v6": "price_xxx_bundle_v2_v6",

    # -----------------------------
    # DEVICES
    # -----------------------------
    "device_low_grade": "price_xxx_device_low_grade",

    # -----------------------------
    # DATABASES
    # -----------------------------
    "virus_database": "price_xxx_virus_db",

    # -----------------------------
    # COURSES (full courses)
    # -----------------------------
    "full_stack_api_course": "price_xxx_full_stack_api",
}
