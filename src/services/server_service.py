from src.models.server import Server, Status, Datacenter
from src.services.repositories_abc import RepositoriesFactoryABC


class ServerService:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._servers = repositories.get_server_repository()
        self._hardwares = repositories.get_hardware_repository()

    async def add_datacenter(
        self, datacenter_name: str, country: str, city: str
    ) -> Datacenter:
        if await self._servers.get_datacenter_by_name(datacenter_name) is not None:
            raise ValueError("Datacenter already exists.")

        datacenter = await self._servers.create_datacenter(
            datacenter_name, country, city
        )
        return datacenter

    async def delete_datacenter(self, datacenter_id: int) -> None:
        await self._servers.delete_datacenter(datacenter_id)

    async def get_datacenters(self) -> list[Datacenter]:
        return await self._servers.get_datacenters()

    async def create_server(
        self,
        datacenter_id: int,
        hardware_id: int,
        status: Status,
        operating_system: str,
    ) -> Server:
        if (
            datacenter := await self._servers.get_datacenter_by_id(datacenter_id)
        ) is None:
            raise ValueError("Datacenter not found.")

        if (hardware := await self._hardwares.get_hardware_by_id(hardware_id)) is None:
            raise ValueError("Hardware not found.")

        server = await self._servers.create_server(
            datacenter, hardware, status, operating_system
        )
        return server

    async def delete_server(self, server_id: int) -> None:
        await self._servers.delete_server(server_id)

    async def change_server_status(self, server_id: int, status: Status) -> None:
        if (server := await self._servers.get_server_by_id(server_id)) is None:
            raise ValueError("Server not found.")

        server.status = status
        await self._servers.save_server(server)

    async def get_servers(self) -> list[Server]:
        return await self._servers.get_servers()
