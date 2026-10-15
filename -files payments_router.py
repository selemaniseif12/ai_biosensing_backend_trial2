warning: in the working copy of 'app/routers/admin_system_router.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/app/routers/admin_system_router.py.bak b/app/routers/admin_system_router.py[m
[1mindex 9c8834a..fb4523f 100644[m
[1m--- a/app/routers/admin_system_router.py.bak[m
[1m+++ b/app/routers/admin_system_router.py[m
[36m@@ -1,82 +1,94 @@[m
[31m-from fastapi import APIRouter, HTTPException[m
[32m+[m[32m﻿from fastapi import APIRouter, Depends, HTTPException[m
 from app.utils.admin_token import validate_admin_token[m
 [m
[32m+[m
[32m+[m[32mdef require_admin_system_token(token: str | None = None):[m
[32m+[m[32m    """Require a valid active admin_system token for every route."""[m
[32m+[m[32m    if not validate_admin_token(token):[m
[32m+[m[32m        raise HTTPException([m
[32m+[m[32m            status_code=403,[m
[32m+[m[32m            detail="Admin token required: admin only",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m
 router = APIRouter([m
     prefix="/admin-system",[m
[31m-    tags=["admin-system"][m
[32m+[m[32m    tags=["admin-system"],[m
[32m+[m[32m    dependencies=[Depends(require_admin_system_token)],[m
 )[m
 [m
[31m-# ---------------------------------------------------[m
[31m-# 1. OUTER GATE — ONLY PLACE WHERE ADMIN TOKEN IS CHECKED[m
[31m-# ---------------------------------------------------[m
 [m
 @router.get("/")[m
[31m-def enter_admin_system(token: str):[m
[31m-    """[m
[31m-    Admin token unlocks the entire Admin & System area.[m
[31m-    Everything inside becomes open.[m
[31m-    """[m
[31m-    if not validate_admin_token(token):[m
[31m-        raise HTTPException(status_code=403, detail="Admin token required: admin only")[m
[32m+[m[32mdef enter_admin_system():[m
     return {"access": "granted", "message": "Welcome to Admin & System"}[m
 [m
 [m
[31m-# ---------------------------------------------------[m
[31m-# 2. INSIDE ADMIN & SYSTEM — ALL DASHBOARDS ARE OPEN[m
[31m-# ---------------------------------------------------[m
[31m-[m
 @router.get("/student")[m
 def admin_student_dashboard():[m
     return {"dashboard": "student", "status": "open"}[m
 [m
[32m+[m
 @router.get("/admin")[m
 def admin_admin_dashboard():[m
     return {"dashboard": "admin", "status": "open"}[m
 [m
[32m+[m
 @router.get("/public")[m
 def admin_public_dashboard():[m
     return {"dashboard": "public", "status": "open"}[m
 [m
[32m+[m
 @router.get("/admin-tokens")[m
 def admin_tokens_dashboard():[m
     return {"dashboard": "admin-tokens", "status": "open"}[m
 [m
[32m+[m
 @router.get("/store")[m
 def admin_store_dashboard():[m
     return {"dashboard": "store", "status": "open"}[m
 [m
[32m+[m
 @router.get("/cart")[m
 def admin_cart_dashboard():[m
     return {"dashboard": "cart", "status": "open"}[m
 [m
[32m+[m
 @router.get("/checkout")[m
 def admin_checkout_dashboard():[m
     return {"dashboard": "checkout", "status": "open"}[m
 [m
[32m+[m
 @router.get("/course-content")[m
 def admin_course_content():[m
     return {"dashboard": "course-content", "status": "open"}[m
 [m
[32m+[m
 @router.get("/course-dashboard")[m
 def admin_course_dashboard():[m
     return {"dashboard": "course-dashboard", "status": "open"}[m
 [m
[32m+[m
 @router.get("/government-admin-viewer")[m
 def admin_government_viewer():[m
     return {"dashboard": "government-admin-viewer", "status": "open"}[m
 [m
[32m+[m
 @router.get("/consulting-history")[m
 def admin_consulting_history():[m
     return {"dashboard": "consulting-history", "status": "open"}[m
 [m
[32m+[m
 @router.get("/consulting-meetings")[m
 def admin_consulting_meetings():[m
     return {"dashboard": "consulting-meetings", "status": "open"}[m
 [m
[32m+[m
 @router.get("/consulting-access")[m
 def admin_consulting_access():[m
     return {"dashboard": "consulting-access", "status": "open"}[m
 [m
[32m+[m
 @router.get("/payment-history")[m
 def admin_payment_history():[m
     return {"dashboard": "payment-history", "status": "open"}[m
[41m+[m
