from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.services.user_service import get_user_by_id
from app.exceptions.user_exceptions import InvalidCredentials
from app.models.user import User
from app.core.security import oauth2_scheme


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        user_id = decode_access_token(token)

        user = get_user_by_id(db, user_id)

        if user is None:
            raise InvalidCredentials()

        return user

    except InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )
       