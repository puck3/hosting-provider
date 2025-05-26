from pydantic import BaseModel, EmailStr


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
