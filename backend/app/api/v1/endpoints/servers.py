from fastapi import APIRouter, Depends

from app.api.v1.schemas.server import CreateDatacenter, CreateServer
from app.db.connector import ServicesFactory, get_services_factory
from app.models.server import Datacenter, Server, Status
from app.services.server_service import ServerService

router = APIRouter(prefix="/servers", tags=["Servers"])


async def get_server_service(
    services: ServicesFactory = Depends(get_services_factory),
) -> ServerService:
    return services.get_server_service()


@router.get("/")
async def get_servers(
    server_service: ServerService = Depends(get_server_service),
) -> list[Server]:
    return server_service.get_servers()


@router.post("/")
async def create_server(
    server: CreateServer,
    server_service: ServerService = Depends(get_server_service),
) -> Server:
    return server_service.create_server(**server.model_dump())


@router.delete("/{server_id}")
async def delete_server(
    server_id: int,
    server_service: ServerService = Depends(get_server_service),
) -> None:
    server_service.delete_server(server_id)


@router.patch("/{server_id}/status")
async def change_server_status(
    server_id: int,
    status: Status,
    server_service: ServerService = Depends(get_server_service),
) -> None:
    server_service.change_server_status(server_id, status)


@router.patch("/release")
async def release_servers(
    server_service: ServerService = Depends(get_server_service),
) -> None:
    server_service.release_servers()


@router.patch("/fix_status")
async def fix_servers_status(
    server_service: ServerService = Depends(get_server_service),
) -> None:
    server_service.fix_servers_status()


@router.get("/datacenters")
async def get_datacenters(
    server_service: ServerService = Depends(get_server_service),
) -> list[Datacenter]:
    return server_service.get_datacenters()


@router.post("/datacenters")
async def add_datacenter(
    datacenter: CreateDatacenter,
    server_service: ServerService = Depends(get_server_service),
) -> Datacenter:
    return server_service.add_datacenter(**datacenter.model_dump())


@router.delete("/datacenters/{datacenter_id}")
async def delete_datacenter(
    datacenter_id: int,
    server_service: ServerService = Depends(get_server_service),
) -> None:
    server_service.delete_datacenter(datacenter_id)
