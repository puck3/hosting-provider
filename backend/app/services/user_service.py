from datetime import date
from passlib.context import CryptContext

from app.core.config import CRYPT_CONTEXT_CONFIG
from app.models.user import User, Role
from app.services.repositories_abc import RepositoriesFactoryABC


class UserService:
    def __init__(self, repositories: RepositoriesFactoryABC):
        self.password_context = CryptContext(**CRYPT_CONTEXT_CONFIG)
        self._users = repositories.get_user_repository()

    def _require_user(self, user_id) -> User:
        if (user := self._users.get_user_by_id(user_id)) is None:
            raise ValueError("User not found.")

        return user

    def _assert_email_is_unique(self, email: str) -> None:
        if self._users.get_user_by_email(email) is not None:
            raise ValueError("Email already registered")

    def _assert_login_is_unique(self, login: str) -> None:
        if self._users.get_user_by_login(login) is not None:
            raise ValueError("Login already registered")

    def _assert_valid_password(self, password: str, password_hash: str):
        if not self.password_context.verify(password, password_hash):
            raise ValueError("Invalid password.")

    def assert_admin_permission(self, user_id: int) -> None:
        user = self._require_user(user_id)
        if not user.is_admin():
            raise PermissionError("Permission denied.")

    def register_user(
        self,
        email: str,
        login: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> User:
        self._assert_email_is_unique(email)
        self._assert_login_is_unique(login)

        password_hash = self.password_context.hash(password)
        user = self._users.create_user(
            email,
            login,
            password_hash,
            first_name,
            last_name,
            birthdate,
        )
        return user

    def login_user(
        self,
        login: str,
        password: str,
    ) -> User:
        if (user := self._users.get_user_by_login(login)) is None:
            raise ValueError("User not found.")

        self._assert_valid_password(password, user.password_hash)
        return user

    def change_user_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> None:
        user = self._require_user(user_id)

        self._assert_valid_password(old_password, user.password_hash)

        user.password_hash = self.password_context.hash(new_password)
        self._users.save_user(user)

    def change_user_email(
        self, user_id: int, password: str, email: str
    ) -> None:
        user = self._require_user(user_id)

        self._assert_valid_password(password, user.password_hash)
        self._assert_email_is_unique(email)

        user.email = email
        self._users.save_user(user)

    def change_user_login(
        self, user_id: int, password: str, login: str
    ) -> None:
        user = self._require_user(user_id)

        self._assert_valid_password(password, user.password_hash)
        self._assert_login_is_unique(login)

        user.login = login
        self._users.save_user(user)

    def change_user_personal(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> None:
        user = self._require_user(user_id)

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if birthdate:
            user.birthdate = birthdate

        self._users.save_user(user)

    def change_user_role_by_email(self, email: str, role: Role) -> None:
        if (user := self._users.get_user_by_email(email)) is None:
            raise ValueError("User not found.")

        user.role = role
        self._users.save_user(user)

    def delete_user(self, user_id: int, password: str) -> None:
        user = self._require_user(user_id)
        self._assert_valid_password(password, user.password_hash)
        self._users.delete_user(user_id)

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self._users.get_user_by_id(user_id)
        return user

    def get_users(self) -> list[User]:
        return self._users.get_users()
