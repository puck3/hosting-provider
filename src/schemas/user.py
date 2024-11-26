from datetime import date
from pydantic import BaseModel

from src.core.constants import default_str, email_str, Role


class Personal(BaseModel):
    first_name: default_str | None
    last_name: default_str | None
    birthdate: date | None


class UserBase(BaseModel):
    email: email_str
    login: default_str
    personal: Personal | None


class UserRequest(UserBase):
    password: default_str


class UserResponse(BaseModel):
    user_id: int | None
    hashed_password: str
    role: Role
