from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import database
from ..db import database_models
from ..schemas.user_models import CreateUser, CreateUserResponse
from ..auth import hash
from ..auth import oauth
from ..utils.enums import Roles, AuthorizationCodes

router = APIRouter(
    prefix="/api/user",
    tags=['User']
)


def create_user_without_password(user: CreateUser, db: Session = Depends(database.get_db)):
    db_user = db.query(database_models.User).filter(
        database_models.User.email == user.email).first()

    if db_user:
        return db_user
    else:
        hashed_password = hash.hash_password(user.phoneNumber)
        user.password = hashed_password

        user.role = Roles.customer

        new_user = database_models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
def create_user(authorizationCode: str, user: CreateUser, db: Session = Depends(database.get_db)):
    # hash user password and replace plain text password with hashed password
    hashed_password = hash.hash_password(user.password)
    user.password = hashed_password

    if authorizationCode not in (AuthorizationCodes.super_admin, AuthorizationCodes.wephco_admin,  AuthorizationCodes.wephco_ceo):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authorization Code")

    new_user = database_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=list[CreateUserResponse])
def get_users(db: Session = Depends(database.get_db)):

    users = db.query(database_models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Users Found")

    return users


@router.get("/{id}", response_model=CreateUserResponse)
def get_user(id: int, db: Session = Depends(database.get_db), current_user: database_models.User = Depends(oauth.get_current_user)):
    user = db.query(database_models.User).filter(
        database_models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.support, Roles.staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Operation not allowed')

    return user


# Implement edit a user by id
@router.put("/{id}", response_model=CreateUserResponse)
def edit_user(id: int, user: CreateUser, db: Session = Depends(database.get_db), current_user: database_models.User = Depends(oauth.get_current_user)):
    db_user = db.query(database_models.User).filter(
        database_models.User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action not authorized")

    db_user.name = user.name
    db_user.email = user.email
    db_user.phoneNumber = user.phoneNumber
    db_user.role = user.role

    db.commit()
    db.refresh(db_user)

    return db_user
