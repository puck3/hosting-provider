import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

POOL_MIN_CONN = int(os.getenv("POOL_MIN_CONN", 1))
POOL_MAX_CONN = int(os.getenv("POOL_MAX_CONN", 10))

CRYPT_CONTEXT_CONFIG = {"schemes": ["bcrypt"], "deprecated": "auto"}

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_CONFIG = {
    "token_type": "access",
    "secret_key": os.getenv("ACCESS_TOKEN_SECRET", "access_secret"),
    "algorithm": ALGORITHM,
    "expires_delta_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE", 15)),
}

REFRESH_TOKEN_CONFIG = {
    "token_type": "refresh",
    "secret_key": os.getenv("REFRESH_TOKEN_SECRET", "refresh_secret"),
    "algorithm": ALGORITHM,
    "expires_delta_minutes": int(
        os.getenv("REFRESH_TOKEN_EXPIRE", 7 * 24 * 60)
    ),
}
