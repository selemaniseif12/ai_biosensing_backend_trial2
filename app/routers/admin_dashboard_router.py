import os
import json
from fastapi import APIRouter, HTTPException
from app.schemas.admin import AdminDashboard, AdminStudent

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)

PROGRESS_BASE_PATH = os.path.join("app", "data", "progress")
TOTAL_MODULES = 10


# ---------------------------------------------------------
# ADMIN DASHBOARD — View all students + completion status
# ---------------------------------------------------------
@router.get("/dashboard", response_model=AdminDashboard)
def admin_dashboard():
    """
    Admin dashboard showing all students, their completed modules,
    and whether they finished the course.
    """

    if not os.path.exists(PROGRESS_BASE_PATH):
        raise HTTPException(status_code=404, detail="No student progress found")

    students = []

    for filename in os.listdir(PROGRESS_BASE_PATH):
        if filename.endswith(".json"):
            file_path = os.path.join(PROGRESS_BASE_PATH, filename)

            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error reading progress file: {str(e)}")

            student_id = data.get("student_id")
            progress_list = data.get("progress", [])

            completed_modules = [
                p["module_id"]
                for p in progress_list
                if p.get("quiz_completed") and p.get("assignment_submitted") and p.get("grade") is not None
            ]

            is_complete = len(completed_modules) == TOTAL_MODULES

            students.append(
                AdminStudent(
                    student_id=student_id,
                    completed_modules=completed_modules,
                    is_course_complete=is_complete
                )
            )

    return AdminDashboard(students=students)
