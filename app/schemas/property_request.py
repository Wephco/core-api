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
    numberOfrooms: int
    budgetRange: str
    maxBudget: str
    notes: Optional[str] = None


class UpdatePropertyRequest(BaseModel):
    userId: int
    location: str
    propertyType: str
    numberOfrooms: int
    budgetRange: str
    maxBudget: str
    isPaid: bool
    notes: Optional[str] = None


class CreatePropertyRequestResponse(BaseModel):
    id: int
    location: str
    propertyType: str
    numberOfrooms: int
    budgetRange: str
    maxBudget: str
    notes: Optional[str] = None
    isPaid: bool
    createdAt: datetime
    userId: int
    user: UserBase
    
    class Config:
        orm_mode = True
