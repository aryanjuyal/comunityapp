from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException


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
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken."
        )

    hashed_password = hash_password(user_data.password)

    db_user = User(
        full_name=user_data.full_name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        profile_image=user_data.profile_image,
        is_active=user_data.is_active,
        is_verified=user_data.is_verified,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
 