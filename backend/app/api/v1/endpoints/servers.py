from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.api.v1.schemas.server import ChangeStatus, Country, CreateDatacenter, CreateServer
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.server import Datacenter, Server
from app.models.user import Role
from app.services.factory import ServicesFactory
from app.services.server_service import ServerService


def assert_is_admin(actor: Actor, error_message: str):
    if actor.role != Role.admin:
        raise HTTPException(HTTP_403_FORBIDDEN, detail=error_message)


async def get_server_service(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> ServerService:
    return services.get_server_service()


servers_router = APIRouter(prefix="/servers", tags=["Servers"])


@servers_router.get("/")
async def get_servers(
    server_service: Annotated[ServerService, Depends(get_server_service)],
) -> list[Server]:
    return server_service.get_servers()


@servers_router.post("/")
async def create_server(
    server: CreateServer,
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Server:
    assert_is_admin(actor, "Only admin can create server.")
    return await server_service.create_server(**server.model_dump())


@servers_router.delete("/{server_id}")
async def delete_server(
    server_id: int,
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    assert_is_admin(actor, "Only admin can delete server.")
    server_service.delete_server(server_id)


@servers_router.patch("/release")
async def release_servers(
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    assert_is_admin(actor, "Only admin can release servers.")
    server_service.release_servers()


@servers_router.patch("/fix_status")
async def fix_servers_status(
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    assert_is_admin(actor, "Only admin can fix servers status.")
    server_service.fix_servers_status()


@servers_router.patch("/{server_id}/status")
async def change_server_status(
    server_id: int,
    status: ChangeStatus,
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    assert_is_admin(actor, "Only admin can change server status.")
    server_service.change_server_status(server_id, **status.model_dump())


datacenters_router = APIRouter(prefix="/datacenters", tags=["Datacenters"])


@datacenters_router.get("/")
async def get_datacenters(
    server_service: Annotated[ServerService, Depends(get_server_service)],
) -> list[Datacenter]:
    return server_service.get_datacenters()


@datacenters_router.get("/countries")
async def get_countries(server_service: Annotated[ServerService, Depends(get_server_service)]) -> list[Country]:
    datacenters = server_service.get_datacenters()
    countries = {datacenter.country for datacenter in datacenters}
    return [Country(country_name=country) for country in countries]


@datacenters_router.post("/")
async def add_datacenter(
    datacenter: CreateDatacenter,
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Datacenter:
    assert_is_admin(actor, "Only admin can create datacenter.")
    return server_service.add_datacenter(**datacenter.model_dump())


@datacenters_router.delete("/{datacenter_id}")
async def delete_datacenter(
    datacenter_id: int,
    server_service: Annotated[ServerService, Depends(get_server_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    assert_is_admin(actor, "Only admin can delete datacenter.")
    server_service.delete_datacenter(datacenter_id)


router = APIRouter()
router.include_router(servers_router)
router.include_router(datacenters_router)
