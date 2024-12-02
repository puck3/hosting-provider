from src.models.hardware import Hardware
from src.models.server import Server, Status
from src.services.repositories_abc import ServerRepositoryABC


class ServerService:
    def __init__(self, servers: ServerRepositoryABC) -> None:
        self._servers = servers

    async def create_server(
        self,
        datacenter_name: str,
        country: str,
        city: str,
        hardware: Hardware,
        status: Status,
        operating_system: str,
    ) -> Server:
        datacenter = await self._servers.get_datacenter_by_name(datacenter_name)
        if datacenter is None:
            datacenter = await self._servers.create_datacenter(
                datacenter_name, country, city
            )
        server = await self._servers.create_server(
            datacenter, hardware, status, operating_system
        )
        return server

    async def update_server_status(self, server: Server, status: Status) -> Server:
        server.update_status(status)
        await self._servers.save_server(server)
        return server

    async def update_server_hardware(
        self, server: Server, hardware: Hardware
    ) -> Server:
        server.update_hardware(Hardware)
        await self._servers.save_server(server)
        return server

    async def update_server_os(self, server: Server, operating_system: str) -> Server:
        server.update_os(operating_system)
        await self._servers.save_server(server)
        return server

    async def get_server_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Server]:
        return await self._servers.get_server_list(skip, limit)
