from passlib.context import CryptContext

from app.core.config import CRYPT_CONTEXT_CONFIG
from app.core.security import JWT
from app.db.redis.token_repository import TokenRepository
from app.models.tokens import Tokens
from app.models.user import User
from app.services.repositories_abc import RepositoriesFactoryABC
from app.utils.logger import logger


class AuthService:
    def __init__(
        self,
        repositories: RepositoriesFactoryABC,
        jwt_access: JWT,
        jwt_refresh: JWT,
        tokens: TokenRepository,
    ):
        self.password_context = CryptContext(**CRYPT_CONTEXT_CONFIG)
        self._users = repositories.get_user_repository()
        self.jwt_access = jwt_access
        self.jwt_refresh = jwt_refresh
        self.tokens = tokens

    async def _get_token_owner(self, token: str) -> User:
        if (user_id := await self.tokens.get_user_id_by_token(token)) is None:
            raise ValueError("Invalid token")

        logger.info(f"Get user_id from redis: {user_id}")

        if (user := self._users.get_user_by_id(user_id)) is None:
            raise ValueError("Token owner not found")

        return user

    async def _create_tokens_pair(self, user: User) -> Tokens:
        access_payload = user.get_access_token_payload()
        access = self.jwt_access.create_token(access_payload)
        refresh_payload = user.get_refresh_token_payload()
        refresh = self.jwt_refresh.create_token(refresh_payload)
        await self.tokens.store_token(refresh, user.user_id)
        return Tokens(access_token=access, refresh_token=refresh)

    def _assert_email_is_unique(self, email: str) -> None:
        if self._users.get_user_by_email(email) is not None:
            raise ValueError("Email already registered")

    def _assert_login_is_unique(self, login: str) -> None:
        if self._users.get_user_by_login(login) is not None:
            raise ValueError("Login already registered")

    def _assert_valid_password(self, password: str, password_hash: str):
        if not self.password_context.verify(password, password_hash):
            raise ValueError("Invalid password.")

    async def login_user(
        self,
        login: str,
        password: str,
    ) -> Tokens:
        if (user := self._users.get_user_by_login(login)) is None:
            raise ValueError("User not found.")

        self._assert_valid_password(password, user.password_hash)
        return await self._create_tokens_pair(user)

    async def refresh_tokens(self, refresh_token: str) -> Tokens:
        user = await self._get_token_owner(refresh_token)
        return await self._create_tokens_pair(user)

    async def change_user_password(self, refresh_token: str, old_password: str, new_password: str) -> Tokens:
        user = await self._get_token_owner(refresh_token)
        self._assert_valid_password(old_password, user.password_hash)
        user.password_hash = self.password_context.hash(new_password)
        self._users.save_user(user)
        return await self._create_tokens_pair(user)

    async def change_user_email(self, refresh_token: str, password: str, email: str) -> Tokens:
        user = await self._get_token_owner(refresh_token)
        self._assert_valid_password(password, user.password_hash)
        self._assert_email_is_unique(email)
        user.email = email
        self._users.save_user(user)
        return await self._create_tokens_pair(user)

    async def change_user_login(self, refresh_token: str, password: str, login: str) -> Tokens:
        user = await self._get_token_owner(refresh_token)
        self._assert_valid_password(password, user.password_hash)
        self._assert_login_is_unique(login)
        user.login = login
        self._users.save_user(user)
        return await self._create_tokens_pair(user)
