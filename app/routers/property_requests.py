from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import PropertyRequest, User
from ..schemas.property_request import CreatePropertyRequest, CreatePropertyRequestResponse
from ..auth.oauth import get_current_user
from typing import List

router = APIRouter(
    prefix="/property-request",
    tags=["Property Requests"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePropertyRequestResponse)
def create_property_request(property_request: CreatePropertyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    new_request = PropertyRequest(userId=user.id, **property_request.dict())
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

    property_request = db.query(PropertyRequest).filter(PropertyRequest.id == id).first()

    if not property_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request does not exist")
    
    return property_request



@router.put("/{id}", response_model=CreatePropertyRequestResponse)
def update_request(id: int, updated_request: CreatePropertyRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    propertyRequestQuery = db.query(PropertyRequest).filter(PropertyRequest.id == id)

    propertyRequest = propertyRequestQuery.first()

    if propertyRequest == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request does not exist")
    
    if propertyRequest.userId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")
    
    propertyRequestQuery.update(updated_request.dict(), synchronize_session=False)

    db.commit()

    return propertyRequestQuery.first()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_request(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    propertyRequestQuery = db.query(PropertyRequest).filter(PropertyRequest.id == id)

    propertyRequest = propertyRequestQuery.first()

    if propertyRequest == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request does not exist")
    
    if propertyRequest.userId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")
    
    propertyRequestQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
