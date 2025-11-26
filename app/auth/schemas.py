# app/auth/schemas.py
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True