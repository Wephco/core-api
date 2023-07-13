from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import DiasporaPropertyListing, User
from ..schemas.diaspora_property_listings import DiasporaPropertyListingBase, DiasporaPropertyListingResponse
from ..auth.oauth import get_current_user
from typing import List
from ..utils.enums import Roles
from .agents import get_agentId_using_agent_name


router = APIRouter(
    prefix="/api/diaspora/property-listings",
    tags=["Diaspora Property Listings"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DiasporaPropertyListingResponse)
async def create_property_listing(property_listing: DiasporaPropertyListingBase, db: Session = Depends(get_db)):

    agent = get_agentId_using_agent_name(property_listing.agentName, db)

    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Agent does not exist. Create agent first before creating a listing')

    property_listing.agentId = agent.id

    new_property_listing = DiasporaPropertyListing(
        location=property_listing.location,
        propertyType=property_listing.propertyType,
        propertyImages=property_listing.propertyImages,
        description=property_listing.description,
        numberOfrooms=property_listing.numberOfrooms,
        numberOfToilets=property_listing.numberOfToilets,
        numberOfBathrooms=property_listing.numberOfBathrooms,
        numberOfLivingRooms=property_listing.numberOfLivingRooms,
        numberOfKitchens=property_listing.numberOfKitchens,
        agentId=agent.id,
    )
    db.add(new_property_listing)
    db.commit()
    db.refresh(new_property_listing)

    return new_property_listing


@router.get('/', response_model=List[DiasporaPropertyListingResponse])
async def get_property_listings(db: Session = Depends(get_db)):

    property_listings = db.query(DiasporaPropertyListing).all()

    return property_listings


@router.get('/{id}', response_model=DiasporaPropertyListingResponse)
async def get_property_listing(id: int, db: Session = Depends(get_db)):

    # if current_user.role not in (Roles.support, Roles.admin, Roles.staff, Roles.super_admin):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    property_listing = db.query(DiasporaPropertyListing).filter(
        DiasporaPropertyListing.id == id).first()

    if not property_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Property Listing not found')

    return property_listing


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=DiasporaPropertyListingResponse)
async def update_property_listing(id: int, property_listing: DiasporaPropertyListingBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    db.query(DiasporaPropertyListing).filter(DiasporaPropertyListing.id == id).update(
        property_listing.dict(), synchronize_session=False)
    db.commit()
    db.refresh(db.query(DiasporaPropertyListing).filter(
        DiasporaPropertyListing.id == id).first())
    updated_property_listing = db.query(DiasporaPropertyListing).filter(
        DiasporaPropertyListing.id == id).first()

    return updated_property_listing


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_property_listing(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    db.query(DiasporaPropertyListing).filter(
        DiasporaPropertyListing.id == id).delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
