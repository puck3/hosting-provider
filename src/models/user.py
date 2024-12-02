from datetime import date
from enum import Enum

from src.models.base import BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    def __init__(
        self,
        user_id: int,
        email: str,
        login: str,
        password_hash: str,
        role: Role,
        first_name: str | None,
        last_name: str | None,
        birthdate: date | None,
    ) -> None:
        self._set_id(user_id)
        self._email = email
        self._login = login
        self._password_hash = password_hash
        self._role = role
        self._first_name = first_name
        self._last_name = last_name
        self._birthdate = birthdate

    def set_email(self, email: str) -> None:
        self._email = email

    def set_password_hash(self, password_hash: str) -> None:
        self._password_hash = password_hash

    def get_password_hash(self) -> str:
        return self._password_hash

    def set_login(self, login: str) -> None:
        self._login = login

    def set_personal(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> None:
        if first_name is not None:
            self._first_name = first_name

        if last_name is not None:
            self._last_name = last_name

        if birthdate is not None:
            self._birthdate = birthdate

    def set_role(self, role: Role) -> None:
        self.role = role

    def is_admin(self):
        return self.role == Role.admin
