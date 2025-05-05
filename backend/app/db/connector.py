import atexit
from psycopg2.pool import SimpleConnectionPool
from app.core.config import DB_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN
from app.db.factory import RepositoriesFactory
from app.services.factory import ServicesFactory

_services_factory: ServicesFactory | None = None
_pool: SimpleConnectionPool | None = None


def initialize_services_factory():
    global _services_factory, _pool
    if _services_factory is not None:
        return

    _pool = SimpleConnectionPool(POOL_MIN_CONN, POOL_MAX_CONN, **DB_CONFIG)
    print("Connection pool initialized.")

    # Инициализируем фабрики
    repositories = RepositoriesFactory(_pool)
    _services_factory = ServicesFactory(repositories)


def get_services_factory() -> ServicesFactory:
    if _services_factory is None:
        raise RuntimeError("Services factory is not initialized.")
    return _services_factory


def close_connection_pool():
    global _pool
    if _pool:
        _pool.closeall()
        print("Connection pool closed.")


atexit.register(close_connection_pool)
