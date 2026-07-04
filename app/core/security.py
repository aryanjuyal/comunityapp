from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt 
from app.core.config import settings
from app.exceptions.user_exceptions import InvalidCredentials
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(
        data:dict,

)->str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
    to_encode.update(
    {
        "exp": expire,
      }# we dont put sub inside thsi function Instead, the caller decides what goes into the payload.
)
    encoded_jwt = jwt.encode(
    to_encode,
    settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
)
    return encoded_jwt
# For example, in the login service:

# access_token = create_access_token(
#     {
#         "sub": str(user.id)
#     }
# )
    
   # Because create_access_token() shouldn't know what kind of token you're creating.
#    we need the secret key in decoding of access token bcz we need to validate the signature of the token to ensure that it was indeed issued by our server and hasn't been tampered with. The secret key is used in the encoding process to create a unique signature for the token. When decoding, we use the same secret key to verify that the signature matches, confirming the token's authenticity and integrity.

def decode_access_token(
    token: str,
) -> str:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidCredentials()

        return user_id

    except jwt.InvalidTokenError:
        raise InvalidCredentials()