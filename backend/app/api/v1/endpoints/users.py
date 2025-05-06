from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.api.v1.schemas.user import (
    ChangeEmail,
    ChangeLogin,
    ChangePassword,
    CreateUser,
    DeleteUser,
    LoginUser,
    Personal,
)
from app.db.connector import ServicesFactory, get_services_factory
from app.models.user import Role, User
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_service(
    services: ServicesFactory = Depends(get_services_factory),
) -> UserService:
    return services.get_user_service()


@router.get("/")
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[User]:
    return user_service.get_users()


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> User | None:
    return user_service.get_user_by_id(user_id)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    password: DeleteUser,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.delete_user(user_id=user_id, **password.model_dump())


@router.post("/")
async def register_user(
    user: CreateUser,
    user_service: UserService = Depends(get_user_service),
) -> User:
    return user_service.register_user(**user.model_dump())


@router.get("/login")
async def login_user(
    user: LoginUser,
    user_service: UserService = Depends(get_user_service),
) -> User:
    return user_service.login_user(**user.model_dump())


@router.patch("/{user_id}/password")
async def change_user_password(
    user_id: int,
    password: ChangePassword,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.change_user_password(
        user_id=user_id, **password.model_dump()
    )


@router.patch("/{user_id}/email")
async def change_user_email(
    user_id: int,
    email: ChangeEmail,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.change_user_email(user_id=user_id, **email.model_dump())


@router.patch("/{user_id}/login")
async def change_user_login(
    user_id: int,
    login: ChangeLogin,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.change_user_login(user_id=user_id, **login.model_dump())


@router.patch("/{user_id}/personal")
async def change_user_personal(
    user_id: int,
    personal: Personal,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.change_user_personal(
        user_id=user_id, **personal.model_dump()
    )


@router.patch("/role/{email}")
async def change_user_role_by_email(
    email: EmailStr,
    role: Role,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return user_service.change_user_role_by_email(email=email, role=role)
