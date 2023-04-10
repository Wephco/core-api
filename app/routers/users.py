from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from db.database import get_db
from db.database_models import User
from ..schemas.user_models import CreateUser, CreateUserResponse
from auth.hash import hash_password
from auth.oauth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # hash user password and replace plain text password with hashed password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=CreateUserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    
    return user
