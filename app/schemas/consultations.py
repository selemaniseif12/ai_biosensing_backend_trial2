from pydantic import BaseModel
from datetime import datetime

class ConsultationBase(BaseModel):
    student_id: int
    team_id: int
    datetime: datetime
    platform: str
    meeting_link: str
    status: str
    notes: str | None = None
    payment_status: str

class ConsultationCreate(ConsultationBase):
    pass

class Consultation(ConsultationBase):
    id: int

    class Config:
        orm_mode = True
