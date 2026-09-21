from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.routers.services import validate_token
from app.models.course_content import CourseContent

router = APIRouter(prefix="/services", tags=["Course Access"])

# ---------------------------------------------------------
# TOKEN CHECK FOR COURSE ACCESS
# ---------------------------------------------------------
def require_course_token(token: str, db: Session = Depends(get_db)):
    """
    Ensures the provided token is active and authorized for course access.
    """
    try:
        validate_token(db, token, "course_access")
    except HTTPException:
        raise HTTPException(status_code=403, detail="Invalid or inactive course access token")
    return True


class CourseAccessRequest(BaseModel):
    token: str


@router.post("/course/{course_id}")
def access_course(
    course_id: str,
    payload: CourseAccessRequest,
    db: Session = Depends(get_db),
    _=Depends(require_course_token)  # token required, logic untouched
):
    # Validate token using your existing validator
    try:
        validate_token(db, payload.token, course_id)
    except HTTPException:
        raise HTTPException(status_code=403, detail="Invalid or inactive token")

    # Fetch course content
    content = (
        db.query(CourseContent)
        .filter(CourseContent.course_id == int(course_id))
        .all()
    )

    return {"course_id": course_id, "content": content}
