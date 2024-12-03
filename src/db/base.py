from contextlib import asynccontextmanager
from typing import AsyncGenerator
from asyncpg import Connection, Pool


class BaseRepository:
    def __init__(self, pool: Pool) -> None:
        if pool is None:
            raise RuntimeError("Connection pool is not initialized.")
        self.__pool = pool

    @asynccontextmanager
    async def _get_connection(self) -> AsyncGenerator[Connection, None]:
        async with self.__pool.acquire() as conn:
            yield conn
