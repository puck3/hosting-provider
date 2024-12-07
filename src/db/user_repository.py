from psycopg2.extras import RealDictCursor
from datetime import date
from src.db.base import BaseRepository
from src.services.repositories_abc import UserRepositoryABC
from src.models.user import User, Role


class UserRepository(BaseRepository, UserRepositoryABC):
    @staticmethod
    def _get_user_from_record(user_record: dict | None) -> User | None:
        if user_record is None:
            return None
        else:
            return User(**user_record)

    def get_user_by_id(self, user_id: int) -> User | None:
        query = """
            SELECT 
                user_id,
                email,
                login,
                password_hash,
                role,
                first_name,
                last_name,
                birthdate
            FROM users
            WHERE user_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()

        return self._get_user_from_record(result)

    def get_user_by_email(self, email: str) -> User | None:
        query = """
            SELECT 
                user_id,
                email,
                login,
                password_hash,
                role,
                first_name,
                last_name,
                birthdate
            FROM users
            WHERE email = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()

        return self._get_user_from_record(result)

    def get_user_by_login(self, login: str) -> User | None:
        query = """
            SELECT 
                user_id,
                email,
                login,
                password_hash,
                role,
                first_name,
                last_name,
                birthdate
            FROM users
            WHERE login = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (login,))
                result = cursor.fetchone()

        return self._get_user_from_record(result)

    def get_users(self) -> list[User]:
        query = """
            SELECT 
                user_id,
                email,
                login,
                password_hash,
                role,
                first_name,
                last_name,
                birthdate
            FROM users
            ORDER BY user_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [self._get_user_from_record(record) for record in result]

    def create_user(
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
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        email,
                        login,
                        password_hash,
                        role,
                        first_name,
                        last_name,
                        birthdate,
                    ),
                )
                user_id = cursor.fetchone()[0]
            conn.commit()

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

    def save_user(self, user: User) -> None:
        query = """
            UPDATE
                users
            SET
                email = %s, login = %s, password_hash = %s, role = %s, first_name = %s, last_name = %s, birthdate = %s
            WHERE
                user_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        user.email,
                        user.login,
                        user.password_hash,
                        user.role,
                        user.first_name,
                        user.last_name,
                        user.birthdate,
                        user.user_id,
                    ),
                )
            conn.commit()

    def delete_user(self, user_id: int) -> None:
        query = """
            DELETE FROM users
            WHERE user_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
            conn.commit()
