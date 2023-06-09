from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import User
from ..schemas.user_models import LoginUser, LoginUserResponse, PasswordReset, CreateUser
from ..auth.hash import verify_password, hash_password
from ..auth.oauth import create_access_token, get_current_user
from ..utils.enums import AuthorizationCodes

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


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


@router.post('/password/reset', status_code=status.HTTP_204_NO_CONTENT, response_model=LoginUserResponse)
def reset_password(authorizationCode: str, body: PasswordReset, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user_query = db.query(User).filter(User.email == body.email)

    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

    if authorizationCode != AuthorizationCodes.super_admin or authorizationCode != AuthorizationCodes.wephco_admin or authorizationCode != AuthorizationCodes.wephco_ceo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authorization Code")

    hashed_password = hash_password(body.password)
    updated_user = CreateUser(name=user.name, email=user.email,
                              phoneNumber=user.phoneNumber, password=hashed_password, role=user.role)
    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()
    db.refresh(user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
