from pydantic import BaseModel, EmailStr
from typing import List
from .property_listings import PropertyListingBase

class AgentBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phoneNumber: str

    class Config:
        orm_mode = True


class AgentResponse(AgentBase):
    id: int
    propertyListings: List[PropertyListingBase]

    class Config:
        orm_mode = True
