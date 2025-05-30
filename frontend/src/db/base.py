from contextlib import contextmanager
from typing import Generator
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection


class BaseRepository:
    def __init__(self, pool: SimpleConnectionPool) -> None:
        if pool is None:
            raise RuntimeError("Connection pool is not initialized.")

        self.__pool = pool

    @contextmanager
    def _get_connection(self) -> Generator[connection, None, None]:
        conn = self.__pool.getconn()
        try:
            yield conn
        finally:
            self.__pool.putconn(conn)
