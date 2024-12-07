from psycopg2.extras import RealDictCursor
from src.db.base import BaseRepository
from src.db.hardware_repository import HardwareRepository
from src.models.hardware import Hardware
from src.models.server import Datacenter, Server, Status
from src.services.repositories_abc import ServerRepositoryABC


class ServerRepository(BaseRepository, ServerRepositoryABC):
    def create_datacenter(
        self, datacenter_name: str, country: str, city: str
    ) -> Datacenter:
        query = """
            INSERT INTO datacenters (
                datacenter_name, country, city 
            )
            VALUES (
                %s, %s, %s
            )
            RETURNING datacenter_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (datacenter_name, country, city))
                datacenter_id = cursor.fetchone()[0]
            conn.commit()

        datacenter = Datacenter(
            datacenter_id=datacenter_id,
            datacenter_name=datacenter_name,
            country=country,
            city=city,
        )
        return datacenter

    def delete_datacenter(self, datacenter_id: int) -> None:
        query = """
            DELETE FROM datacenters
            WHERE datacenter_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (datacenter_id,))
            conn.commit()

    @staticmethod
    def _get_datacenter_from_record(record: dict | None) -> Datacenter | None:
        if record is None:
            return None
        else:
            return Datacenter(**record)

    def get_datacenter_by_id(self, datacenter_id: int) -> Datacenter | None:
        query = """
            SELECT
                datacenter_id,
                datacenter_name,
                country,
                city
            FROM datacenters
            WHERE datacenter_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (datacenter_id,))
                result = cursor.fetchone()

        return self._get_datacenter_from_record(result)

    def get_datacenter_by_name(self, datacenter_name: str) -> Datacenter | None:
        query = """
            SELECT
                datacenter_id,
                datacenter_name,
                country,
                city
            FROM datacenters
            WHERE datacenter_name = %s; 
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (datacenter_name,))
                result = cursor.fetchone()

        return self._get_datacenter_from_record(result)

    def get_datacenters(self) -> list[Datacenter]:
        query = """
            SELECT
                datacenter_id,
                datacenter_name,
                country,
                city
            FROM datacenters
            ORDER BY datacenter_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [self._get_datacenter_from_record(record) for record in result]

    def create_server(
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
                %s, %s, %s, %s
            )
            RETURNING server_id;
        """
        datacenter_id = datacenter.datacenter_id
        hardware_id = hardware.hardware_id
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query, (datacenter_id, hardware_id, status, operating_system)
                )
                server_id = cursor.fetchone()[0]
                conn.commit()

        server = Server(
            server_id=server_id,
            datacenter=datacenter,
            hardware=hardware,
            status=status,
            operating_system=operating_system,
        )
        return server

    def save_server(self, server: Server) -> None:
        query = """
            UPDATE servers
            SET
                datacenter_id = %s, hardware_id = %s, status = %s, operating_system = %s
            WHERE
                server_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        server.datacenter.datacenter_id,
                        server.hardware.hardware_id,
                        server.status,
                        server.operating_system,
                        server.server_id,
                    ),
                )
            conn.commit()

    def delete_server(self, server_id: int) -> None:
        query = """
            DELETE FROM servers
            WHERE server_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (server_id,))
            conn.commit()

    @staticmethod
    def get_server_from_record(record: dict | None) -> Server | None:
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

    def get_server_by_id(self, server_id: int) -> Server | None:
        query = """
            SELECT 
                s.server_id,
                s.status,
                s.operating_system,
                d.datacenter_id,
                d.datacenter_name,
                d.country,
                d.city,
                h.hardware_id,
                h.cpu_id,
                h.cpu_name,
                h.cpu_vendor,
                h.cores,
                h.frequency,
                h.cpus_count,
                h.gpu_id,
                h.gpu_name,
                h.gpu_vendor,
                h.vram_type,
                h.vram_gb,
                h.gpus_count,
                h.storage_tb,
                h.ram_gb,
                h.bandwidth_gbps
            FROM 
                servers s
                LEFT JOIN datacenters d USING (datacenter_id)
                LEFT JOIN extended_hardwares h USING (hardware_id)
            WHERE 
                s.server_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (server_id,))
                result = cursor.fetchone()

        return self.get_server_from_record(result)

    def get_servers(self):
        query = """
            SELECT 
                s.server_id,
                s.status,
                s.operating_system,
                d.datacenter_id,
                d.datacenter_name,
                d.country,
                d.city,
                h.hardware_id,
                h.cpu_id,
                h.cpu_name,
                h.cpu_vendor,
                h.cores,
                h.frequency,
                h.cpus_count,
                h.gpu_id,
                h.gpu_name,
                h.gpu_vendor,
                h.vram_type,
                h.vram_gb,
                h.gpus_count,
                h.storage_tb,
                h.ram_gb,
                h.bandwidth_gbps
            FROM
                servers s
                LEFT JOIN datacenters d USING (datacenter_id)
                LEFT JOIN extended_hardwares h USING (hardware_id)
            ORDER BY s.server_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [self.get_server_from_record(record) for record in result]

    def reserve_server(self, hardware_id: int, country: str) -> int:
        query = """
            WITH updated_server AS (
                SELECT 
                    server_id
                FROM 
                    servers
                    JOIN datacenters USING (datacenter_id)
                WHERE
                    hardware_id = %s 
                    AND country = %s
                    AND status = %s
                LIMIT 1
            )
            UPDATE servers
            SET status = %s
            WHERE server_id = (SELECT server_id FROM updated_server)
            RETURNING server_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query, (hardware_id, country, Status.available, Status.rented)
                )
                reserved_server_id = cursor.fetchone()[0]
            conn.commit()

        return reserved_server_id

    def release_servers(self) -> None:
        query = """
            WITH unused_servers AS (
                SELECT server_id
                FROM servers
                WHERE
                    status = %s
                    AND server_id NOT IN (
                        SELECT server_id
                        FROM rentals
                        WHERE 
                            end_at > CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'
                    )
            )
            UPDATE servers
            SET status = %s
            WHERE server_id in (SELECT server_id FROM unused_servers);
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (Status.rented, Status.available))
            conn.commit()

    def fix_servers_status(self) -> None:
        query = """
            UPDATE servers
            SET status = %s
            WHERE status != %s 
            AND server_id in (
                SELECT server_id 
                FROM rentals 
                WHERE end_at > CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'
            )
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (Status.rented, Status.rented))
            conn.commit()
