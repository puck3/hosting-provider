from datetime import date

from pydantic import BaseModel, EmailStr

from app.models.user import Role, User


class CreateUser(BaseModel):
    email: EmailStr
    login: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    birthdate: str | None = None


class LoginUser(BaseModel):
    login: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ChangeEmail(BaseModel):
    password: str
    email: EmailStr


class ChangeLogin(BaseModel):
    password: str
    login: str


class Personal(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: str | None = None


class DeleteUser(BaseModel):
    password: str


class ChangeRole(BaseModel):
    role: Role


class ReadUser(BaseModel):
    user_id: int
    email: str
    login: str
    role: Role
    first_name: str | None
    last_name: str | None
    birthdate: date | None

    @staticmethod
    def from_user(user: User) -> "ReadUser":
        return ReadUser(
            user_id=user.user_id,
            email=user.email,
            login=user.login,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            birthdate=user.birthdate,
        )
