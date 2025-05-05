from psycopg2.extras import RealDictCursor
from src.models.hardware import CPU, GPU, Hardware
from src.services.repositories_abc import HardwareRepositoryABC
from src.db.base import BaseRepository


class HardwareRepository(BaseRepository, HardwareRepositoryABC):
    @staticmethod
    def _get_cpu_from_record(record: dict | None) -> CPU | None:
        if record is None:
            return None
        else:
            return CPU(**record)

    @staticmethod
    def _get_gpu_from_record(record: dict | None) -> GPU | None:
        if record is None:
            return None
        else:
            return GPU(**record)

    @staticmethod
    def get_hardware_from_record(record: dict | None) -> Hardware | None:
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
                GPU(**gpu_data) if gpu_data.get("gpu_id") is not None else None
            )

            return Hardware(**hardware_data)

    def get_cpu_by_id(self, cpu_id: int) -> CPU | None:
        query = """
            SELECT
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency
            FROM cpus
            WHERE cpu_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (cpu_id,))
                result = cursor.fetchone()

        return self._get_cpu_from_record(result)

    def get_cpu_by_name(self, cpu_name: str) -> CPU | None:
        query = """
            SELECT
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency
            FROM cpus
            WHERE cpu_name = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (cpu_name,))
                result = cursor.fetchone()

        return self._get_cpu_from_record(result)

    def get_cpus(self) -> list[CPU]:
        query = """
            SELECT
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency
            FROM cpus
            ORDER BY cpu_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [
            cpu
            for cpu in (self._get_cpu_from_record(record) for record in result)
            if cpu is not None
        ]

    def create_cpu(
        self, cpu_name: str, cpu_vendor: str, cores: int, frequency: float
    ) -> CPU:
        query = """
            INSERT INTO cpus (
                cpu_name, cpu_vendor, cores, frequency
            )
            VALUES (%s, %s, %s, %s)
            RETURNING cpu_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (cpu_name, cpu_vendor, cores, frequency))
                result = cursor.fetchone()
            conn.commit()

        if result is None:
            raise RuntimeError("Failed to create CPU")

        cpu_id = result[0]

        cpu = CPU(
            cpu_id=cpu_id,
            cpu_name=cpu_name,
            cpu_vendor=cpu_vendor,
            cores=cores,
            frequency=frequency,
        )
        return cpu

    def delete_cpu(self, cpu_id: int) -> None:
        query = """
            DELETE FROM cpus
            WHERE cpu_id = %s; 
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (cpu_id,))
            conn.commit()

    def get_gpu_by_id(self, gpu_id: int) -> GPU | None:
        query = """
            SELECT
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb
            FROM gpus
            WHERE gpu_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (gpu_id,))
                result = cursor.fetchone()

        return self._get_gpu_from_record(result)

    def get_gpu_by_name(self, gpu_name: str) -> GPU | None:
        query = """
            SELECT
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb
            FROM gpus
            WHERE gpu_name = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (gpu_name,))
                result = cursor.fetchone()

        return self._get_gpu_from_record(result)

    def get_gpus(self) -> list[GPU]:
        query = """
            SELECT
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb
            FROM gpus
            ORDER BY gpu_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [
            gpu
            for gpu in (self._get_gpu_from_record(record) for record in result)
            if gpu is not None
        ]

    def create_gpu(
        self, gpu_name: str, gpu_vendor: str, vram_type: str, vram_gb: int
    ) -> GPU:
        query = """
            INSERT INTO gpus (
                gpu_name, gpu_vendor, vram_type, vram_gb
            )
            VALUES (%s, %s, %s, %s)
            RETURNING gpu_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query, (gpu_name, gpu_vendor, vram_type, vram_gb)
                )
                result = cursor.fetchone()
            conn.commit()

        if result is None:
            raise RuntimeError("Failed to create GPU")

        gpu_id = result[0]

        gpu = GPU(
            gpu_id=gpu_id,
            gpu_name=gpu_name,
            gpu_vendor=gpu_vendor,
            vram_type=vram_type,
            vram_gb=vram_gb,
        )
        return gpu

    def delete_gpu(self, gpu_id: int) -> None:
        query = """
            DELETE FROM gpus
            WHERE gpu_id = %s; 
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (gpu_id,))
            conn.commit()

    def get_hardware_by_id(self, hardware_id: int) -> Hardware | None:
        query = """
            SELECT
                hardware_id,
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency,
                cpus_count,
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb,
                gpus_count,
                storage_tb,
                ram_gb,
                bandwidth_gbps
            FROM extended_hardwares
            WHERE hardware_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (hardware_id,))
                result = cursor.fetchone()

        return self.get_hardware_from_record(result)

    def get_hardwares(self) -> list[Hardware]:
        query = """
            SELECT
                hardware_id,
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency,
                cpus_count,
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb,
                gpus_count,
                storage_tb,
                ram_gb,
                bandwidth_gbps
            FROM extended_hardwares
            ORDER BY hardware_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [
            hw
            for hw in (
                self.get_hardware_from_record(record) for record in result
            )
            if hw is not None
        ]

    def create_hardware(
        self,
        cpu: CPU,
        cpus_count: int,
        storage_tb: int,
        ram_gb: int,
        bandwidth_gbps: int,
        gpu: GPU | None = None,
        gpus_count: int = 0,
    ) -> Hardware:
        query = """
            INSERT INTO hardwares (
                cpu_id, cpus_count, gpu_id, gpus_count, storage_tb, ram_gb,bandwidth_gbps 
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING hardware_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        cpu.cpu_id,
                        cpus_count,
                        gpu.gpu_id if gpu else None,
                        gpus_count,
                        storage_tb,
                        ram_gb,
                        bandwidth_gbps,
                    ),
                )
                result = cursor.fetchone()
                conn.commit()

            if result is None:
                raise RuntimeError("Failed to create hardware")

            hardware_id = result[0]

        hardware = Hardware(
            hardware_id=hardware_id,
            cpu=cpu,
            cpus_count=cpus_count,
            gpu=gpu,
            gpus_count=gpus_count,
            storage_tb=storage_tb,
            ram_gb=ram_gb,
            bandwidth_gbps=bandwidth_gbps,
        )
        return hardware

    def delete_hardware(self, hardware_id: int) -> None:
        query = """
            DELETE FROM hardwares
            WHERE hardware_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (hardware_id,))
            conn.commit()
