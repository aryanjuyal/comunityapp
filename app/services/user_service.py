from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password
from fastapi import HTTPException
from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    UsernameAlreadyExists,
)
def get_user_by_id(
    db: Session,
    user_id: str,
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

def authenticate_user(
      db:Session,
      user_data:UserLogin
):
    user = get_user_by_email(db, user_data.email)

    if user is None:
        raise InvalidCredentials()

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise InvalidCredentials()

    return user
def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )
# if we find the email it will get a aqlalchemy object otherwiase NONE

def get_user_by_username(db:Session,username:str,):
    return (
        db.query(User).filter(User.username==username).first()
    )

def create_user(
    db: Session,
    user_data: UserCreate,
):
    print("Reached create_user")
    if get_user_by_email(db, user_data.email):
        raise EmailAlreadyExists()

    if get_user_by_username(db, user_data.username):
        raise UsernameAlreadyExists()

    hashed_password = hash_password(user_data.password)

    db_user = User(
        full_name=user_data.full_name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
       
    )

    db.add(db_user)
    print("Before commit")
    db.commit()

    print("After commit")
    db.refresh(db_user)

    return db_user