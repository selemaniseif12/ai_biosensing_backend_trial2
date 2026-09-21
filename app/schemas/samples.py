from pydantic import BaseModel


class SampleBase(BaseModel):
    customer_id: int
    description: str


class SampleCreate(SampleBase):
    pass


class SampleUpdate(SampleBase):
    pass


class SampleResponse(SampleBase):
    id: int

    class Config:
        orm_mode = True
