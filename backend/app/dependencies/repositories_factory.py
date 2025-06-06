from typing import Annotated

from fastapi import Depends
from psycopg2.pool import SimpleConnectionPool

from app.db.connector import get_connection_pool
from app.db.factory import RepositoriesFactory
from app.services.repositories_abc import RepositoriesFactoryABC


def get_repositories_factory(
    connection_pool: Annotated[
        SimpleConnectionPool, Depends(get_connection_pool)
    ],
) -> RepositoriesFactoryABC:
    return RepositoriesFactory(connection_pool)
