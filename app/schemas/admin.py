from pydantic import BaseModel
from typing import List, Optional

class AdminStudent(BaseModel):
    student_id: str
    completed_modules: List[int]
    is_course_complete: bool

class AdminDashboard(BaseModel):
    students: List[AdminStudent]
