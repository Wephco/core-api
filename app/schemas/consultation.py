from pydantic import BaseModel, EmailStr
from .user_models import UserBase
from datetime import datetime


class ConsultationBase(BaseModel):
    name: str
    location: str
    phoneNumber: str
    email: EmailStr
    message: str
    contactMethod: str

    class Config:
        orm_mode = True


class ConsultationResponse(ConsultationBase):
    id: int
    userId: int
    user: UserBase
    createdAt: datetime

    class Config:
        orm_mode = True
