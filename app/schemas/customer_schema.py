# app/schemas/customer_schema.py

from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: str
