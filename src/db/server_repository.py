from asyncpg import Record
from src.db.base import BaseRepository
from src.db.hardware_repository import HardwareRepository
from src.models.hardware import Hardware
from src.models.server import Datacenter, Server, Status
from src.services.repositories_abc import ServerRepositoryABC


class ServerRepository(BaseRepository, ServerRepositoryABC):
    async def create_datacenter(
        self, datacenter_name: str, country: str, city: str
    ) -> Datacenter:
        query = """
            INSERT INTO datacenters (
                datacenter_name, country, city 
            )
            VALUES (
                $1, $2, $3
            )
            RETURNING datacenter_id;
        """
        async with self._get_connection() as conn:
            datacenter_id = await conn.fetchval(query, datacenter_name, country, city)

        datacenter = Datacenter(
            datacenter_id=datacenter_id,
            datacenter_name=datacenter_name,
            country=country,
            city=city,
        )
        return datacenter

    async def delete_datacenter(self, datacenter_id: int) -> None:
        query = """
            DELETE FROM datacenters
            WHERE datacenter_id = $1;
        """
        async with self._get_connection() as conn:
            await conn.execute(query, datacenter_id)

    @staticmethod
    def _get_datacenter_from_record(record: Record | None) -> Datacenter | None:
        if record is None:
            return None
        else:
            return Datacenter(**record)

    async def get_datacenter_by_id(self, datacenter_id: int) -> Datacenter | None:
        query = """
            SELECT *
            FROM datacenters
            WHERE datacenter_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, datacenter_id)

        return self._get_datacenter_from_record(result)

    async def get_datacenter_by_name(self, datacenter_name: str) -> Datacenter | None:
        query = """
            SELECT *
            FROM datacenters
            WHERE datacenter_name = $1; 
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, datacenter_name)

        return self._get_datacenter_from_record(result)

    async def get_datacenters(self) -> list[Datacenter]:
        query = """
            SELECT *
            FROM datacenters;
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self._get_datacenter_from_record(record) for record in result]

    async def create_server(
        self,
        datacenter: Datacenter,
        hardware: Hardware,
        status: Status,
        operating_system: str,
    ) -> Server:
        query = """
            INSERT INTO servers (
                datacenter_id, hardware_id, status, operating_system
            )
            VALUES (
                $1, $2, $3, $4
            )
            RETURNING server_id;
        """
        datacenter_id = datacenter.datacenter_id
        hardware_id = hardware.hardware_id
        async with self._get_connection() as conn:
            server_id = await conn.fetchval(
                query, datacenter_id, hardware_id, status, operating_system
            )

        server = Server(
            server_id=server_id,
            datacenter=datacenter,
            hardware=hardware,
            status=status,
            operating_system=operating_system,
        )
        return server

    async def save_server(self, server: Server) -> None:
        query = """
            UPDATE servers
            SET
                datacenter_id = $1, hardware_id = $2, status = $3, operating_system = $4
            WHERE
                server_id = $5;
        """
        async with self._get_connection() as conn:
            await conn.execute(
                query,
                server.datacenter.datacenter_id,
                server.hardware.hardware_id,
                server.status,
                server.operating_system,
            )

    async def delete_server(self, server_id: int) -> None:
        query = """
            DELETE FROM servers
            WHERE server_id = $1;
        """
        async with self._get_connection() as conn:
            await conn.execute(query, server_id)

    @staticmethod
    def get_server_from_record(record: Record | None) -> Server | None:
        if record is None:
            return None
        else:
            server_data = {
                key: value
                for key, value in record.items()
                if key in Server.model_fields.keys()
            }
            datacenter_data = {
                key: value
                for key, value in record.items()
                if key in Datacenter.model_fields.keys()
            }
            server_data["datacenter"] = Datacenter(**datacenter_data)
            server_data["hardware"] = HardwareRepository.get_hardware_from_record(
                record
            )
            return Server(**server_data)

    async def get_server_by_id(self, server_id: int) -> Server | None:
        query = """
            SELECT 
                *
            FROM 
                servers
                LEFT JOIN datacenters USING (datacenter_id)
                LEFT JOIN extended_hardwares USING (hardware_id)
            WHERE 
                server_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, server_id)

        return self.get_server_from_record(result)

    async def get_servers(self):
        query = """
            SELECT 
                *
            FROM
                servers
                LEFT JOIN datacenters USING (datacenter_id)
                LEFT JOIN extended_hardwares USING (hardware_id)
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self.get_server_From_record(record) for record in result]

    async def reserve_server(self, hardware_id: int, country: str) -> int:
        query = """
            WITH updated_server AS (
                SELECT 
                    server_id
                FROM 
                    servers
                    JOIN datacenters USING (datacenter_id)
                WHERE
                    hardware_id = $1 
                    AND country = $2
                    AND status = 'inactive'
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            )
            UPDATE servers
            SET status = 'active'
            WHERE server_id = (SELECT server_id FROM updated_server)
            RETURNING server_id;
        """
        async with self._get_connection() as conn:
            reserved_server_id = await conn.fetchval(query, hardware_id, country)

        return reserved_server_id
