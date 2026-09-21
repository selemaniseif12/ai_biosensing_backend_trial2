from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    description: str
    price: int
    duration: str
    category: str
    status: str

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode
