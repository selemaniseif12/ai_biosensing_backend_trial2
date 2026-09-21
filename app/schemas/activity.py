# app/schemas/activity.py

from datetime import datetime
from pydantic import BaseModel


class ActivityBase(BaseModel):
    user_id: int
    course_id: int
    module_id: int | None = None
    content_id: int | None = None
    action: str


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    module_id: int | None
    content_id: int | None
    action: str
    timestamp: datetime

    class Config:
        orm_mode = True
