from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..schemas.user_models import UserBase


class HotelRequestBase(BaseModel):
    checkInDate: str
    checkOutDate: str
    name: str
    phone: str
    email: EmailStr
    numberOfGuests: int
    numberOfRooms: int
    budgetPerRoom: int
    notes: Optional[str] = None


class HotelRequestResponse(BaseModel):
    id: int
    checkInDate: str
    checkOutDate: str
    name: str
    phone: str
    email: EmailStr
    numberOfGuests: int
    numberOfRooms: int
    budgetPerRoom: int
    isPaid: bool
    createdAt: datetime
    userId: int
    user: UserBase

    class Config:
        orm_mode = True


class UpdateHotelRequest(HotelRequestBase):
    id: int
    isPaid: bool
    userId: int
