from datetime import date
from passlib.context import CryptContext

from src.core.config import CRYPT_CONTEXT_CONFIG
from src.models.user import User, Role
from src.services.repositories_abc import UserRepositoryABC


class UserService:
    def __init__(self, users: UserRepositoryABC):
        self.password_context = CryptContext(**CRYPT_CONTEXT_CONFIG)
        self._users = users

    async def _assert_email_is_unique(self, email: str) -> None:
        if await self._users.get_user_by_email(email) is not None:
            raise ValueError("Email already registered")

    async def _assert_login_is_unique(self, login: str) -> None:
        if await self._users.get_user_by_login(login) is not None:
            raise ValueError("Login already registered")

    @staticmethod
    def assert_admin_permission(user: User) -> None:
        if not user.is_admin:
            raise PermissionError("Permission denied.")

    def assert_valid_password(self, password: str, password_hash: str):
        if not self.password_context.verify(password, password_hash):
            raise ValueError("Invalid password")

    async def register_user(
        self,
        email: str,
        login: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> User:
        await self._assert_email_is_unique(email)
        await self._assert_login_is_unique(login)

        password_hash = self.password_context.hash(password)
        user = await self._users.create_user(
            email,
            login,
            password_hash,
            first_name,
            last_name,
            birthdate,
        )
        return user

    async def change_user_password(
        self, user: User, old_password: str, new_password: str
    ) -> User:
        self.assert_valid_password(old_password, user.get_password_hash())
        user.set_password_hash(self.password_context.hash(new_password))
        await self._users.save_user(user)
        return user

    async def change_user_email(self, user: User, password: str, email: str) -> User:
        self.assert_valid_password(password, user.get_password_hash())
        await self._assert_email_is_unique(email)

        user.set_email(email)
        await self._users.save_user(user)
        return user

    async def change_user_login(self, user: User, password: str, login: str) -> User:
        self.assert_valid_password(password, user.get_password_hash())
        await self._assert_login_is_unique(login)

        user.set_login(login)
        await self._users.save_user(user)
        return user

    async def change_user_personal(
        self,
        user: User,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> User:
        user.set_personal(first_name, last_name, birthdate)
        await self._users.save_user(user)
        return user

    async def change_user_role(self, admin: User, user: User, role: Role) -> User:
        self.assert_admin_permission(admin)

        user.set_role(role)
        await self._users.save_user(user)
        return user

    async def delete_user(self, user: User, password):
        self.assert_valid_password(password, user.get_password_hash())
        await self._users.delete_user(user)
