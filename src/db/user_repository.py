from asyncpg import Record
from datetime import date
from src.db.base import BaseRepository
from src.services.user_service import UserRepositoryABC
from src.models.user import User, Role


class UserRepository(BaseRepository, UserRepositoryABC):
    @staticmethod
    def _get_user_from_record(user_record: Record | None) -> User | None:
        if user_record is None:
            return None
        else:
            return User(**user_record)

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = """
            SELECT *
            FROM users
            WHERE user_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, user_id)

        return self._get_user_from_record(result)

    async def get_user_by_email(self, email: str) -> User | None:
        query = """
            SELECT *
            FROM users
            WHERE email = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, email)

        return self._get_user_from_record(result)

    async def get_user_by_login(self, login: str) -> User | None:
        query = """
            SELECT *
            FROM users
            WHERE login = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, login)

        return self._get_user_from_record(result)

    async def create_user(
        self,
        email: str,
        login: str,
        password_hash: str,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
        role: Role = Role.user,
    ) -> User:
        query = """
            INSERT INTO users (
                email, login, password_hash, role, first_name, last_name, birthdate
            )
            VALUES (
               $1, $2, $3, $4, $5, $6, $7
            )
            RETURNING user_id;
        """
        async with self._get_connection() as conn:
            user_id = await conn.fetchval(
                query,
                email,
                login,
                password_hash,
                role,
                first_name,
                last_name,
                birthdate,
            )

        user = User(
            user_id=user_id,
            email=email,
            login=login,
            password_hash=password_hash,
            role=role,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
        )
        return user

    async def save_user(self, user: User) -> None:
        query = """
            UPDATE
                users
            SET
                email = $1, login = $2, password_hash = $3, role = $4, first_name = $5, last_name = $6, birthdate = $7
            WHERE
                user_id = $8;
        """
        async with self._get_connection() as conn:
            await conn.execute(
                query,
                user.email,
                user.login,
                user.password_hash,
                user.role,
                user.first_name,
                user.last_name,
                user.birthdate,
                user.user_id,
            )

    async def delete_user(self, user_id: int) -> None:
        query = """
            DELETE FROM users
            WHERE user_id = $1;
        """
        async with self._get_connection() as conn:
            await conn.execute(query, user_id)
