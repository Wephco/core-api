from pydantic import BaseModel, EmailStr
from typing import Any, List
from datetime import datetime
from .agents import AgentBase


class PropertyListingBase(BaseModel):
    location: str
    propertyType: str
    propertyImages: List[str]
    numberOfrooms: int
    numberOfToilets: int
    numberOfBathrooms: int
    numberOfLivingRooms: int
    numberOfKitchens: int
    agentId: int

    class Config:
        orm_mode = True


class PropertyListingResponse(PropertyListingBase):
    id: int
    createdAt: datetime
    agentId: int
    agent: AgentBase

    class Config:
        orm_mode = True
