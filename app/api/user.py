
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from Backend.app.core.security import verify_password
from app.db.dependencies import get_db
from app.services.user_service import authenticate_user, create_user, get_user_by_email
from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    UsernameAlreadyExists,
)
from app.schemas.user import UserCreate, UserLogin,UserResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
@router.post("/login",response_model=UserResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, user_data)
        return user

    except InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )
@router.post("/register",
response_model=UserResponse,
status_code=201)

def register_user(user_data:UserCreate,
db:Session =  Depends(get_db)):
    try:
        user=create_user(db,user_data)
        return user


    except EmailAlreadyExists:
        raise HTTPException(
        status_code=409,
        detail="Email already registered."
    )



    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="USername already taken",
        )


