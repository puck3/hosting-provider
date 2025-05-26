from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_403_FORBIDDEN

from app.api.v1.endpoints.servers import assert_is_admin
from app.api.v1.schemas.user import (
    CreateUser,
    DeleteUser,
    Personal,
)
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.user import Role, User
from app.services.factory import ServicesFactory
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_service(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> UserService:
    return services.get_user_service()


@router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> list[User]:
    assert_is_admin(actor, "Only admin can get users.")
    return user_service.get_users()


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> User | None:
    if (actor.user_id != user_id) and (actor.role != Role.admin):
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            detail="Only owner or admin can get user by id.",
        )
    return user_service.get_user_by_id(user_id)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    password: DeleteUser,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.user_id != user_id:
        raise HTTPException(HTTP_403_FORBIDDEN)
    return user_service.delete_user(user_id=user_id, **password.model_dump())


@router.post("/")
async def register_user(
    user: CreateUser,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    return user_service.create_user(**user.model_dump())


@router.patch("/{user_id}/personal")
async def change_user_personal(
    user_id: int,
    personal: Personal,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.user_id != user_id:
        raise HTTPException(HTTP_403_FORBIDDEN)
    return user_service.change_user_personal(user_id=user_id, **personal.model_dump())


@router.patch("/role/{email}")
async def change_user_role_by_email(
    email: EmailStr,
    role: Role,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.role != Role.admin:
        raise HTTPException(HTTP_403_FORBIDDEN, detail="Only admin can change role.")
    return user_service.change_user_role_by_email(email=email, role=role)
