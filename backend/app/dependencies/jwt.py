from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import ACCESS_TOKEN_CONFIG, REFRESH_TOKEN_CONFIG
from app.core.security import JWT

access_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/refresh",
    scheme_name="access_token",
)

refresh_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="refresh_token",
)


def get_access_token(token: Annotated[str, Depends(access_scheme)]) -> str:
    return token


def get_refresh_token(
    token: Annotated[str, Depends(refresh_scheme)],
) -> str:
    return token


def get_jwt_access() -> JWT:
    return JWT(**ACCESS_TOKEN_CONFIG)


def get_jwt_refresh() -> JWT:
    return JWT(**REFRESH_TOKEN_CONFIG)
