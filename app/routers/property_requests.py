from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import PropertyRequest, User
from ..schemas.property_request import UpdatePropertyRequest, CreatePropertyRequestResponse, PropertyRequestBase
from ..schemas.user_models import CreateUser
from ..auth.oauth import get_current_user
from .users import create_user_without_password
from typing import List
from ..utils.enums import Roles


router = APIRouter(
    prefix="/property-request",
    tags=["Property Requests"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePropertyRequestResponse)
async def create_property_request(property_request: PropertyRequestBase, db: Session = Depends(get_db)):

    new_user = CreateUser(name=property_request.name, email=property_request.email,
                          phoneNumber=property_request.phoneNumber, password=property_request.phoneNumber)
    user = create_user_without_password(new_user, db)

    new_request = PropertyRequest(userId=user.id, location=property_request.location, propertyType=property_request.propertyType,
                                  numberOfrooms=property_request.numberOfrooms, budgetRange=property_request.budgetRange, maxBudget=property_request.maxBudget, isPaid=False)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.get("/", response_model=List[CreatePropertyRequestResponse])
def get_property_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    propertyRequests = db.query(PropertyRequest).all()
    return propertyRequests


@router.get("/{id}", response_model=CreatePropertyRequestResponse)
def get_property_request(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    property_request = db.query(PropertyRequest).filter(
        PropertyRequest.id == id).first()

    if not property_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request not Found")

    return property_request


@router.put("/{id}", response_model=CreatePropertyRequestResponse)
def update_request(id: int, updated_request: UpdatePropertyRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    propertyRequestQuery = db.query(
        PropertyRequest).filter(PropertyRequest.id == id)

    propertyRequest = propertyRequestQuery.first()

    if propertyRequest == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request does not exist")

    if current_user.role == Roles.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")

    propertyRequestQuery.update(
        updated_request.dict(), synchronize_session=False)

    db.commit()

    return propertyRequestQuery.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_request(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    propertyRequestQuery = db.query(
        PropertyRequest).filter(PropertyRequest.id == id)

    propertyRequest = propertyRequestQuery.first()

    if propertyRequest == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request does not exist")

    if current_user.role == Roles.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")

    propertyRequestQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
