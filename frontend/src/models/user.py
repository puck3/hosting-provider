from datetime import date
from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    user_id: int
    email: str
    login: str
    role: Role
    first_name: str | None
    last_name: str | None
    birthdate: date | None

    def is_admin(self) -> bool:
        return self.role == Role.admin
