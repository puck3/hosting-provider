from app.db.redis.publisher import Publisher
from app.models.server import Datacenter, Server, Status
from app.services.repositories_abc import RepositoriesFactoryABC


class ServerService:
    def __init__(self, repositories: RepositoriesFactoryABC, publisher: Publisher) -> None:
        self._servers = repositories.get_server_repository()
        self._hardwares = repositories.get_hardware_repository()
        self._publisher = publisher

    def add_datacenter(self, datacenter_name: str, country: str, city: str) -> Datacenter:
        if self._servers.get_datacenter_by_name(datacenter_name) is not None:
            raise ValueError("Datacenter already exists.")

        datacenter = self._servers.create_datacenter(datacenter_name, country, city)
        return datacenter

    def delete_datacenter(self, datacenter_id: int) -> None:
        self._servers.delete_datacenter(datacenter_id)

    def get_datacenters(self) -> list[Datacenter]:
        return self._servers.get_datacenters()

    async def create_server(
        self,
        datacenter_id: int,
        hardware_id: int,
        status: Status,
        operating_system: str,
    ) -> Server:
        if (datacenter := self._servers.get_datacenter_by_id(datacenter_id)) is None:
            raise ValueError("Datacenter not found.")

        if (hardware := self._hardwares.get_hardware_by_id(hardware_id)) is None:
            raise ValueError("Hardware not found.")

        server = self._servers.create_server(datacenter, hardware, status, operating_system)

        await self._publisher.publish_event(
            "server_created", {"server_id": server.server_id, "datacenter_id": datacenter_id}
        )

        return server

    def delete_server(self, server_id: int) -> None:
        self._servers.delete_server(server_id)

    def change_server_status(self, server_id: int, status: Status) -> None:
        if (server := self._servers.get_server_by_id(server_id)) is None:
            raise ValueError("Server not found.")

        server.status = status
        self._servers.save_server(server)

    def get_servers(self) -> list[Server]:
        return self._servers.get_servers()

    def release_servers(self) -> None:
        self._servers.release_servers()

    def fix_servers_status(self) -> None:
        self._servers.fix_servers_status()
