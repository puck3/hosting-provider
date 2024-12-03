from asyncpg import create_pool
from contextlib import asynccontextmanager
from src.core.config import DB_CONFIG
from src.db.repositories_factory import RepositoriesFactory
from src.services.services_factory import ServicesFactory

services_factory: ServicesFactory | None = None


@asynccontextmanager
async def lifespan():
    global services_factory
    async with create_pool(**DB_CONFIG) as pool:
        print("Connection pool initialized.")
        repositories = RepositoriesFactory(pool)
        services_factory = ServicesFactory(repositories)
        yield
        print("Connection pool closed.")


def get_services_factory() -> RepositoriesFactory:
    if services_factory is None:
        raise RuntimeError("Factory is not initialized.")
    return services_factory
