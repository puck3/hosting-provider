from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.v1.schemas.token import Token
from app.api.v1.schemas.user import (
    ChangeEmail,
    ChangeLogin,
    ChangePassword,
)
from app.dependencies.jwt import get_refresh_token
from app.dependencies.services_factory import get_services_factory
from app.services.factory import AuthService, ServicesFactory


router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_auth_service(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> AuthService:
    return services.get_auth_service()


@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
) -> Token:
    try:
        tokens = auth.login_user(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True
    )
    return Token(access_token=tokens.access_token)


@router.get("/refresh")
async def refresh_token(
    refresh_token: Annotated[str, Depends(get_refresh_token)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
) -> Token:
    try:
        tokens = auth.refresh_tokens(refresh_token)
    except ValueError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True
    )
    return Token(access_token=tokens.access_token)


@router.patch("/refresh/password")
async def change_user_password(
    refresh_token: Annotated[str, Depends(get_refresh_token)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    password: ChangePassword,
) -> Token:
    try:
        tokens = auth.change_user_password(
            refresh_token, **password.model_dump()
        )
    except ValueError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True
    )
    return Token(access_token=tokens.access_token)


@router.patch("/refresh/email")
async def change_user_email(
    refresh_token: Annotated[str, Depends(get_refresh_token)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    email: ChangeEmail,
) -> Token:
    try:
        tokens = auth.change_user_email(refresh_token, **email.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True
    )
    return Token(access_token=tokens.access_token)


@router.patch("/refresh/login")
async def change_user_login(
    refresh_token: Annotated[str, Depends(get_refresh_token)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    login: ChangeLogin,
) -> Token:
    try:
        tokens = auth.change_user_login(refresh_token, **login.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="refresh_token", value=tokens.refresh_token, httponly=True
    )
    return Token(access_token=tokens.access_token)
