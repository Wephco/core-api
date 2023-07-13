from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import User, Consultation
from ..schemas.consultation import ConsultationBase, ConsultationResponse
from ..schemas.user_models import CreateUser
from ..auth.oauth import get_current_user
from typing import List
from ..utils.enums import Roles
from .users import create_user_without_password

router = APIRouter(
    prefix="/api/consultations",
    tags=["Consultations"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ConsultationResponse)
async def create_consultation_request(consultation_request: ConsultationBase, db: Session = Depends(get_db)):

    new_user = CreateUser(name=consultation_request.name, email=consultation_request.email,
                          phoneNumber=consultation_request.phoneNumber, password=consultation_request.phoneNumber)
    
    user = create_user_without_password(new_user, db)

    new_request = Consultation(userId=user.id,
                               service=consultation_request.service,
                               message=consultation_request.message,
                               contactMethod=consultation_request.contactMethod
                               )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.get("/", response_model=List[ConsultationResponse])
def get_all_consultation_requests(db: Session = Depends(get_db)):

    consultationRequests = db.query(Consultation).all()
    return consultationRequests


@router.get("/{id}", response_model=ConsultationResponse)
def get_a_consultation_request(id: int, db: Session = Depends(get_db)):

    consultation_request = db.query(Consultation).filter(
        Consultation.id == id).first()

    # if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff, Roles.support):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    if not consultation_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request not Found")

    return consultation_request


@router.put("/{id}", response_model=ConsultationResponse)
def update_a_request(id: int, updated_request: ConsultationBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    consultationRequestQuery = db.query(
        Consultation).filter(Consultation.id == id)

    consultationRequest = consultationRequestQuery.first()

    if consultationRequest == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Request does not exist")

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")

    consultationRequestQuery.update(
        updated_request.dict(), synchronize_session=False)

    db.commit()

    return consultationRequestQuery.first()
