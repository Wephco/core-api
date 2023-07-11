from pydantic import BaseModel
from typing import List
from datetime import datetime


class DiasporaPropertyListingBase(BaseModel):
    location: str
    propertyType: str
    propertyImages: List[str]
    numberOfrooms: int
    numberOfToilets: int
    numberOfBathrooms: int
    numberOfLivingRooms: int
    numberOfKitchens: int
    agentId: int
    agentName: str

    class Config:
        orm_mode = True


class DiasporaPropertyListingResponse(DiasporaPropertyListingBase):
    id: int
    createdAt: datetime
    agentId: int
    agentName: str

    class Config:
        orm_mode = True
