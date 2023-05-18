from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import PropertyListing, User
from ..schemas.property_listings import PropertyListingBase, PropertyListingResponse
from ..auth.oauth import get_current_user
from typing import List
from ..utils.enums import Roles


router = APIRouter(
    prefix="/property-listings",
    tags=["Property Listings"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PropertyListingResponse)
async def create_property_listing(property_listing: PropertyListingBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.agent or Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    new_property_listing = PropertyListing(**property_listing.dict())
    db.add(new_property_listing)
    db.commit()
    db.refresh(new_property_listing)

    return new_property_listing


@router.get('/', response_model=List[PropertyListingResponse])
async def get_property_listings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.agent or Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    property_listings = db.query(PropertyListing).all()

    return property_listings


@router.get('/{id}', response_model=PropertyListingResponse)
async def get_property_listing(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.agent or Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    property_listing = db.query(PropertyListing).filter(
        PropertyListing.id == id).first()

    if not property_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Property Listing not found')

    return property_listing


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PropertyListingResponse)
async def update_property_listing(id: int, property_listing: PropertyListingBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.agent or Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    db.query(PropertyListing).filter(PropertyListing.id == id).update(
        property_listing.dict(), synchronize_session=False)
    db.commit()
    db.refresh(db.query(PropertyListing).filter(
        PropertyListing.id == id).first())
    updated_property_listing = db.query(PropertyListing).filter(
        PropertyListing.id == id).first()

    return updated_property_listing


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_property_listing(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.agent or Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    db.query(PropertyListing).filter(
        PropertyListing.id == id).delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
