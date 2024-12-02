import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "min_size": int(os.getenv("POOL_MIN_CONN", 1)),
    "max_size": int(os.getenv("POOL_MAX_CONN", 10)),
}

CRYPT_CONTEXT_CONFIG = {"schemes": ["pbkdf2_sha256"], "deprecated": "auto"}
