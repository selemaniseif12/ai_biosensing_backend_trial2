from pydantic import BaseModel
from typing import List

class ModuleBase(BaseModel):
    course_id: int
    module_number: int
    title: str
    description: str
    video_description: str
    slide_description: str
    pdf_description: str
    website_description: str
    lessons: List[str]
    quiz: str
    quiz_file: str
    assignment: str
    assignment_file: str

class ModuleCreate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    id: int

    class Config:
        from_attributes = True

