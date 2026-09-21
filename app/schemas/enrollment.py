# app/schemas/enrollment.py

from datetime import datetime
from pydantic import BaseModel


class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int
    status: str = "active"


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
