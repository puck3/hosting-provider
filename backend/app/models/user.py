from pydantic import BaseModel
from datetime import date
from enum import Enum


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    user_id: int
    email: str
    login: str
    password_hash: str
    role: Role
    first_name: str | None
    last_name: str | None
    birthdate: date | None

    def is_admin(self) -> bool:
        return self.role == Role.admin

    def get_refresh_token_payload(self) -> dict:
        return {"sub": str(self.user_id)}

    def get_access_token_payload(self) -> dict:
        return {"sub": str(self.user_id), "role": self.role.value}
