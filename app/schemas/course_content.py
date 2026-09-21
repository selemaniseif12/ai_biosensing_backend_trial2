from pydantic import BaseModel

class CourseContentCreate(BaseModel):
    course_id: int
    module_number: int
    video: str
    slides_pdf: str
    website: str
    quiz_file: str

class CourseContentResponse(BaseModel):
    id: int
    course_id: int
    module_number: int
    video: str
    slides_pdf: str
    website: str
    quiz_file: str

    class Config:
        orm_mode = True
