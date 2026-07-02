from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import model_validator
from sqlalchemy import UUID


class UserCreate(BaseModel):
    class UserResponse(BaseModel):
        id: UUID

    full_name: str

    username: str

    email: EmailStr

    profile_image: str | None

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
         from_attributes=True 
     )#what it does is it converts the  sqlalchemy object into what fastapi wants tells Pydantic:

# "You are allowed to read attributes from normal Python objects." a sqlalchemy object is not a table but a pytho object that represents one row of a table

    full_name: str = Field(
        min_length=3,
        max_length=100
    )

    username: str = Field(
        min_length=3,
        max_length=30
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=64
    )

    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self):

        if self.password != self.confirm_password:
            raise ValueError(
                "Passwords do not match."
            )

        return self