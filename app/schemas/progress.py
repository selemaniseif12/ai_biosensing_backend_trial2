from pydantic import BaseModel
from typing import List, Optional

class ModuleProgress(BaseModel):
    module_id: int
    quiz_completed: bool = False
    assignment_submitted: bool = False
    grade: Optional[float] = None
    feedback: Optional[str] = None

class StudentProgress(BaseModel):
    student_id: str
    progress: List[ModuleProgress]
