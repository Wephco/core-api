from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import User
from ..schemas.user_models import LoginUser, LoginUserResponse, PasswordReset, CreateUser
from ..auth.hash import verify_password, hash_password
from ..auth.oauth import create_access_token
# from ..utils.enums import AuthorizationCodes

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=LoginUserResponse)
def register(user: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=LoginUserResponse)
def login(user_credentials: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create token and send to user
    access_token = create_access_token(
        data={"userId": user.id, "role": user.role})

    return {
        "name": user.name,
        "email": user.email,
        "phoneNumber": user.phoneNumber,
        "token": access_token
    }


# Implement password reset
@router.post("/password-reset", status_code=status.HTTP_200_OK)
def password_reset(password_reset: PasswordReset, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == password_reset.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    hashed_password = hash_password(password_reset.password)
    user.password = hashed_password

    db.commit()

    return Response(status_code=status.HTTP_200_OK)

