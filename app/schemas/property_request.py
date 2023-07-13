from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..schemas.user_models import UserBase


class PropertyRequestBase(BaseModel):
    name: str
    email: EmailStr
    phoneNumber: str
    location: str
    propertyType: str
    requestType: str
    budget: str
    preferredService: str
    isPaid: Optional[bool] = False


class UpdatePropertyRequest(BaseModel):
    id: int
    userId: int
    location: str
    propertyType: str
    requestType: str
    budget: str
    isPaid: bool

    class Config:
        orm_mode = True


class CreatePropertyRequestResponse(BaseModel):
    id: int
    location: str
    propertyType: str
    requestType: str
    budget: str
    preferredService: str
    isPaid: bool
    createdAt: datetime
    userId: int
    user: UserBase

    class Config:
        orm_mode = True
