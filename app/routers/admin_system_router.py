from fastapi import APIRouter, HTTPException
from app.utils.admin_token import validate_admin_token

router = APIRouter(
    prefix="/admin-system",
    tags=["admin-system"]
)

# ---------------------------------------------------
# 1. OUTER GATE — ONLY PLACE WHERE ADMIN TOKEN IS CHECKED
# ---------------------------------------------------

@router.get("/")
def enter_admin_system(token: str):
    """
    Admin token unlocks the entire Admin & System area.
    Everything inside becomes open.
    """
    if not validate_admin_token(token):
        raise HTTPException(status_code=403, detail="Admin token required: admin only")
    return {"access": "granted", "message": "Welcome to Admin & System"}


# ---------------------------------------------------
# 2. INSIDE ADMIN & SYSTEM — ALL DASHBOARDS ARE OPEN
# ---------------------------------------------------

@router.get("/student")
def admin_student_dashboard():
    return {"dashboard": "student", "status": "open"}

@router.get("/admin")
def admin_admin_dashboard():
    return {"dashboard": "admin", "status": "open"}

@router.get("/public")
def admin_public_dashboard():
    return {"dashboard": "public", "status": "open"}

@router.get("/admin-tokens")
def admin_tokens_dashboard():
    return {"dashboard": "admin-tokens", "status": "open"}

@router.get("/store")
def admin_store_dashboard():
    return {"dashboard": "store", "status": "open"}

@router.get("/cart")
def admin_cart_dashboard():
    return {"dashboard": "cart", "status": "open"}

@router.get("/checkout")
def admin_checkout_dashboard():
    return {"dashboard": "checkout", "status": "open"}

@router.get("/course-content")
def admin_course_content():
    return {"dashboard": "course-content", "status": "open"}

@router.get("/course-dashboard")
def admin_course_dashboard():
    return {"dashboard": "course-dashboard", "status": "open"}

@router.get("/government-admin-viewer")
def admin_government_viewer():
    return {"dashboard": "government-admin-viewer", "status": "open"}

@router.get("/consulting-history")
def admin_consulting_history():
    return {"dashboard": "consulting-history", "status": "open"}

@router.get("/consulting-meetings")
def admin_consulting_meetings():
    return {"dashboard": "consulting-meetings", "status": "open"}

@router.get("/consulting-access")
def admin_consulting_access():
    return {"dashboard": "consulting-access", "status": "open"}

@router.get("/payment-history")
def admin_payment_history():
    return {"dashboard": "payment-history", "status": "open"}
