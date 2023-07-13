from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DiasporaPropertyListingBase(BaseModel):
    location: str
    propertyType: str
    propertyImages: List[str]
    description: Optional[str] = ''
    numberOfrooms: int
    numberOfToilets: int
    numberOfBathrooms: int
    numberOfLivingRooms: int
    numberOfKitchens: int
    agentId: int
    agentName: Optional[str] = ''

    class Config:
        orm_mode = True


class DiasporaPropertyListingResponse(DiasporaPropertyListingBase):
    id: int
    createdAt: datetime
    agentId: int

    class Config:
        orm_mode = True
