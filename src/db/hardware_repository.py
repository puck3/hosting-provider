from re import I
from asyncpg import Record
from src.models.hardware import CPU, GPU, Hardware
from src.services.repositories_abc import HardwareRepositoryABC
from src.db.base import BaseRepository


class HardwareRepository(BaseRepository, HardwareRepositoryABC):
    @staticmethod
    def _get_cpu_from_record(record: Record | None) -> CPU | None:
        if record is None:
            return None
        else:
            return CPU(**record)

    @staticmethod
    def _get_gpu_from_record(record: Record | None) -> GPU | None:
        if record is None:
            return None
        else:
            return GPU(**record)

    @staticmethod
    def get_hardware_from_record(record: Record | None) -> Hardware | None:
        if record is None:
            return None
        else:
            hardware_data = {
                key: value
                for key, value in record.items()
                if key in Hardware.model_fields.keys()
            }

            cpu_data = {
                key: value
                for key, value in record.items()
                if key in CPU.model_fields.keys()
            }
            hardware_data["cpu"] = CPU(**cpu_data)

            gpu_data = {
                key: value
                for key, value in record.items()
                if key in GPU.model_fields.keys()
            }
            hardware_data["gpu"] = (
                GPU(**gpu_data) if gpu_data["gpu_id"] is not None else None
            )

            return Hardware(**hardware_data)

    async def get_cpu_by_id(self, cpu_id: int) -> CPU | None:
        query = """
            SELECT *
            FROM cpus
            WHERE cpu_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, cpu_id)

        return self._get_cpu_from_record(result)

    async def get_cpu_by_name(self, cpu_name: str) -> CPU | None:
        query = """
            SELECT *
            FROM cpus
            WHERE cpu_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, cpu_name)

        return self._get_cpu_from_record(result)

    async def get_cpus(self) -> list[CPU]:
        query = """
            SELECT *
            FROM cpus; 
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self._get_cpu_from_record(record) for record in result]

    async def create_cpu(
        self, cpu_name: str, cpu_vendor: str, cores: int, frequency: float
    ) -> CPU:
        query = """
            INSERT INTO cpus (
                cpu_name, cpu_vendor, cores, frequency
            )
            VALUES (
                $1, $2, $3, $4
            )
            RETURNING cpu_id;
        """
        async with self._get_connection() as conn:
            cpu_id = await conn.fetchval(query, cpu_name, cpu_vendor, cores, frequency)

        cpu = CPU(
            cpu_id=cpu_id,
            cpu_name=cpu_name,
            cpu_vendor=cpu_vendor,
            cores=cores,
            frequency=frequency,
        )
        return cpu

    async def delete_cpu(self, cpu_id: int) -> None:
        query = """
            DELETE FROM cpus
            WHERE cpu_id = $1; 
        """
        async with self._get_connection() as conn:
            conn.execute(query, cpu_id)

    async def get_gpu_by_id(self, gpu_id: int) -> GPU | None:
        query = """
            SELECT *
            FROM gpus
            WHERE gpu_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, gpu_id)

        return self._get_gpu_from_record(result)

    async def get_gpu_by_name(self, gpu_name: str) -> GPU | None:
        query = """
            SELECT *
            FROM gpus
            WHERE gpu_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, gpu_name)

        return self._get_gpu_from_record(result)

    async def get_gpus(self) -> list[GPU]:
        query = """
            SELECT *
            FROM gpus; 
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self._get_gpu_from_record(record) for record in result]

    async def create_gpu(
        self, gpu_name: str, gpu_vendor: str, vram_type: str, vram_gb: int
    ):
        query = """
            INSERT INTO gpus (
                gpu_name, gpu_vendor, vram_type, vram_gb
            )
            VALUES (
                $1, $2, $3, $4
            )
            RETURNING gpu_id;
        """
        async with self._get_connection() as conn:
            gpu_id = await conn.fetchval(
                query, gpu_name, gpu_vendor, vram_type, vram_gb
            )

        gpu = GPU(
            gpu_id=gpu_id,
            gpu_name=gpu_name,
            gpu_vendor=gpu_vendor,
            vram_type=vram_type,
            vram_gb=vram_gb,
        )
        return gpu

    async def delete_gpu(self, gpu_id: int) -> None:
        query = """
            DELETE FROM gpus
            WHERE gpu_id = $1; 
        """
        async with self._get_connection() as conn:
            conn.execute(query, gpu_id)

    async def get_hardware_by_id(self, hardware_id: int) -> Hardware | None:
        query = """
            SELECT *
            FROM extended_hardwares
            WHERE hardware_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, hardware_id)

        return self.get_hardware_from_record(result)

    async def get_hardwares(self) -> list[Hardware]:
        query = """
            SELECT *
            FROM extended_hardwares
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self.get_hardware_from_record(record) for record in result]

    async def create_hardware(
        self,
        cpu: CPU,
        cpus_count: int,
        storage_gb: int,
        ram_gb: int,
        bandwidth_mbps: int,
        gpu: GPU | None = None,
        gpus_count: int = 0,
    ):
        query = """
            INSERT INTO hardwares (
                cpu_id, cpus_count, gpu_id, gpus_count, storage_gb, ram_gb, bandwidth_mbps
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7
            )
            RETURNING hardware_id;
        """
        async with self._get_connection() as conn:
            hardware_id = await conn.fetchval(
                query,
                cpu.cpu_id,
                cpus_count,
                gpu.gpu_id if gpu is not None else None,
                gpus_count,
                storage_gb,
                ram_gb,
                bandwidth_mbps,
            )
        hardware = Hardware(
            hardware_id=hardware_id,
            cpu=cpu,
            cpus_count=cpus_count,
            gpu=gpu,
            gpus_count=gpus_count,
            storage_gb=storage_gb,
            ram_gb=ram_gb,
            bandwidth_mbps=bandwidth_mbps,
        )
        return hardware

    async def delete_hardware(self, hardware_id: int) -> None:
        query = """
            DELETE FROM hardwares
            WHERE hardware_id = $1;
        """
        async with self._get_connection() as conn:
            await conn.execute(query, hardware_id)
