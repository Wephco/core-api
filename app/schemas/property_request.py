from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PropertyRequestBase(BaseModel):
    location: str
    propertyType: str
    numberOfrooms: int
    budgetRange: str
    maxBudget: str
    notes: Optional[str] = None


class CreatePropertyRequest(PropertyRequestBase):
    userId: int


class CreatePropertyRequestResponse(PropertyRequestBase):
    id: int
    isPaid: bool
    userId: int
    createdAt: datetime

    class Config:
        orm_mode = True