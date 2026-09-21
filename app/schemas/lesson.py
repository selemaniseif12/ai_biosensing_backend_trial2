# app/schemas/lesson.py

from pydantic import BaseModel
from typing import List, Optional

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    slides_urls: Optional[List[str]] = None

class LessonCreate(LessonBase):
    pass

class LessonRead(LessonBase):
    id: int
    module_id: int

    class Config:
        orm_mode = True
