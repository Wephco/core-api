from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import User
from ..schemas.user_models import LoginUser, LoginUserResponse
from ..auth.hash import verify_password
from ..auth.oauth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=LoginUserResponse)
def login(user_credentials: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # create token and send to user
    access_token = create_access_token(data={"userId":user.id})

    return {
    "name": user.name,
    "email": user.email,
    "phoneNumber": user.phoneNumber,
    "token": access_token
    }