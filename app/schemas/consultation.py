from pydantic import BaseModel, EmailStr
from .user_models import UserBase
from datetime import datetime


class ConsultationBase(BaseModel):
    name: str
    phoneNumber: str
    email: EmailStr
    service: str
    message: str
    contactMethod: str

    class Config:
        orm_mode = True


class ConsultationResponse(ConsultationBase):
    id: int
    userId: int
    createdAt: datetime

    class Config:
        orm_mode = True
