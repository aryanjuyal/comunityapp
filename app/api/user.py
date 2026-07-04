
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.security import create_access_token, verify_password
from app.db.dependencies import get_db
from app.services.user_service import authenticate_user, create_user, get_user_by_email
from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    UsernameAlreadyExists,
)
from app.schemas.user import Token, UserCreate, UserLogin,UserResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
@router.post("/login",response_model=Token, status_code=200)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, user_data)
        access_token=create_access_token({"sub":str(user.id)})
        return{
            "access_token":access_token,
            "token_type":"bearer",
        }

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
            status_code=400,
            detail="Email already exists.",
        )
    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        ) 


  


