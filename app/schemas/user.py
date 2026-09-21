from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserOut(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
