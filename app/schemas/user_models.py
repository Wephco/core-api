from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .api_response import ApiResponse

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phoneNumber: str


class CreateUser(UserBase):
    password: str


class CreateUserResponse(UserBase):
    id: int
    createdAt: datetime

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(UserBase):
    token: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

