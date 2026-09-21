import os
import json
from fastapi import APIRouter, HTTPException
from app.schemas.progress import StudentProgress, ModuleProgress

router = APIRouter(
    prefix="/students",
    tags=["Student Progress Tracking"]
)

PROGRESS_BASE_PATH = os.path.join("app", "data", "progress")


# ---------------------------------------------------------
# 1. UPDATE STUDENT PROGRESS (POST)
# ---------------------------------------------------------
@router.post("/{student_id}/progress/update")
def update_progress(student_id: str, module_progress: ModuleProgress):
    """
    Update progress for a student for a specific module.
    Saves progress as JSON in app/data/progress/.
    """

    os.makedirs(PROGRESS_BASE_PATH, exist_ok=True)

    file_path = os.path.join(PROGRESS_BASE_PATH, f"{student_id}.json")

    # Load existing progress if available
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = {"student_id": student_id, "progress": []}

    # Remove old entry for this module
    existing_data["progress"] = [
        p for p in existing_data["progress"]
        if p["module_id"] != module_progress.module_id
    ]

    # Add updated module progress
    existing_data["progress"].append(module_progress.dict())

    # Save back to file
    try:
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        return {
            "status": "success",
            "message": "Progress updated successfully",
            "student_id": student_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving progress: {str(e)}")


# ---------------------------------------------------------
# 2. RETRIEVE STUDENT PROGRESS (GET)
# ---------------------------------------------------------
@router.get("/{student_id}/progress", response_model=StudentProgress)
def get_progress(student_id: str):
    """
    Retrieve full progress for a student.
    """

    file_path = os.path.join(PROGRESS_BASE_PATH, f"{student_id}.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="No progress found for this student")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading progress file: {str(e)}")
