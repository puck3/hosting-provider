from psycopg2.pool import SimpleConnectionPool

from app.core.config import DB_CONFIG, POOL_MAX_CONN, POOL_MIN_CONN

_pool: SimpleConnectionPool | None = None


def initialize_connection():
    global _pool
    _pool = SimpleConnectionPool(POOL_MIN_CONN, POOL_MAX_CONN, **DB_CONFIG)
    print("Connection pool initialized.")


def get_connection_pool() -> SimpleConnectionPool:
    if _pool is None:
        raise RuntimeError("Connection pool is not initialized.")
    return _pool


def close_connection_pool():
    global _pool
    if _pool:
        _pool.closeall()
        print("Connection pool closed.")
