from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import HotelRequest, User
from ..schemas.hotel_requests import HotelRequestBase, HotelRequestResponse, UpdateHotelRequest
from ..schemas.user_models import CreateUser
from ..auth.oauth import get_current_user
from .users import create_user_without_password
from typing import List
from ..utils.enums import Roles


router = APIRouter(
    prefix='/api/hotel-request',
    tags=['Hotel Request']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=HotelRequestResponse)
async def create_hotel_request(hotel_request: HotelRequestBase, db: Session = Depends(get_db)):

    new_user = CreateUser(name=hotel_request.name, email=hotel_request.email,
                          phoneNumber=hotel_request.phone, password=hotel_request.phone)

    user = create_user_without_password(new_user, db)

    new_request = HotelRequest(userId=user.id, checkInDate=hotel_request.checkInDate, checkOutDate=hotel_request.checkOutDate, name=hotel_request.name, phone=hotel_request.phone, email=hotel_request.email,
                               numberOfGuests=hotel_request.numberOfGuests, numberOfRooms=hotel_request.numberOfRooms, budgetPerRoom=hotel_request.budgetPerRoom, isPaid=False)

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.get('/', response_model=List[HotelRequestResponse])
async def get_all_hotel_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    hotel_requests = db.query(HotelRequest).all()
    return hotel_requests


@router.get('/{id}', response_model=HotelRequestResponse)
async def get_a_hotel_request(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    hotel_request = db.query(HotelRequest).filter(
        HotelRequest.id == id).first()

    if not hotel_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Request not Found')

    return hotel_request


@router.put('/{id}', response_model=HotelRequestResponse)
async def update_a_hotel_request(id: int, updated_request: UpdateHotelRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    hotel_request_query = db.query(HotelRequest).filter(HotelRequest.id == id)

    if not hotel_request_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Request not Found')

    if current_user.role == Roles.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    hotel_request_query.update(
        updated_request.dict(), synchronize_session=False)
    db.commit()
    db.refresh(hotel_request_query.first())

    return hotel_request_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_hotel_request(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    hotel_request_query = db.query(HotelRequest).filter(HotelRequest.id == id)

    if not hotel_request_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Request not Found')

    if current_user.role == Roles.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    hotel_request_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
