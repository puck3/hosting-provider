from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.api.v1.endpoints.servers import assert_is_admin
from app.api.v1.schemas.user import ChangeRole, CreateUser, DeleteUser, Personal, ReadUser
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.user import Role
from app.services.factory import ServicesFactory
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_service(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> UserService:
    return services.get_user_service()


@router.get("/self")
async def get_self(
    user_service: Annotated[UserService, Depends(get_user_service)], actor: Annotated[Actor, Depends(get_actor)]
) -> ReadUser:
    user = user_service.get_user_by_id(actor.user_id)
    if user is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="User not found.")
    return ReadUser.from_user(user)


@router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> list[ReadUser]:
    assert_is_admin(actor, "Only admin can get users.")
    return [ReadUser.from_user(user) for user in user_service.get_users()]


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> ReadUser:
    if (actor.user_id != user_id) and (actor.role != Role.admin):
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            detail="Only owner or admin can get user by id.",
        )
    if (user := user_service.get_user_by_id(user_id)) is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="User not found.")
    return ReadUser.from_user(user)


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
) -> ReadUser:
    new_user = user_service.create_user(**user.model_dump())
    return ReadUser.from_user(new_user)


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
    role: ChangeRole,
    user_service: Annotated[UserService, Depends(get_user_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.role != Role.admin:
        raise HTTPException(HTTP_403_FORBIDDEN, detail="Only admin can change role.")
    return user_service.change_user_role_by_email(email=email, **role.model_dump())
