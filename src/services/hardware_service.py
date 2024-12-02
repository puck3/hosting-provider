from src.models.hardware import Hardware, CPU, GPU
from src.services.repositories_abc import HardwareRepositoryABC


class HardwareService:
    def __init__(self, hardwares: HardwareRepositoryABC) -> None:
        self._hardwares = hardwares

    async def _find_or_create_gpu(
        self,
        gpu_name: str | None,
        gpu_vendor: str | None,
        vram_type: str | None,
        vram_gb: int | None,
        gpus_count: int,
    ) -> GPU:
        if gpus_count == 0:
            gpu = None
        elif (
            gpu_name is not None
            or gpu_vendor is not None
            or vram_type is not None
            or vram_gb is not None
        ):
            gpu = await self._hardwares.get_gpu_by_name(gpu_name)
            if gpu is None:
                gpu = await self._hardwares.create_gpu(
                    gpu_name, gpu_vendor, vram_type, vram_gb
                )
        else:
            raise ValueError("Invalid gpu.")

        return gpu

    async def _find_or_create_cpu(
        self,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
    ) -> CPU:
        cpu = await self._hardwares.get_cpu_by_name(cpu_name)
        if cpu is None:
            cpu = await self._hardwares.create_cpu(
                cpu_name, cpu_vendor, cores, frequency
            )

        return cpu

    async def create_hardware(
        self,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
        cpus_count: int,
        storage_gb: int,
        ram_gb: int,
        bandwidth_mbps: int,
        gpu_name: int | None = None,
        gpu_vendor: str | None = None,
        vram_type: str | None = None,
        vram_gb: str | None = None,
        gpus_count: int = 0,
    ) -> Hardware:
        cpu = await self._find_or_create_cpu(cpu_name, cpu_vendor, cores, frequency)
        gpu = await self._find_or_create_gpu(
            gpu_name, gpu_vendor, vram_type, vram_gb, gpus_count
        )

        hardware = await self._hardwares.create_hardware(
            cpu, cpus_count, storage_gb, ram_gb, bandwidth_mbps, gpu, gpus_count
        )
        return hardware

    async def get_hardware_list(self, skip: int, limit: int) -> list[Hardware]:
        return await self._hardwares.get_hardware_list(skip, limit)

    async def get_cpu_list(self, skip: int, limit: int) -> list[CPU]:
        return await self._hardwares.get_cpu_list(skip, limit)

    async def get_gpu_list(self, skip: int, limit: int) -> list[GPU]:
        return await self._hardwares.get_gpu_list(skip, limit)

    async def update_gpu(
        self,
        hardware: Hardware,
        gpu_id: int | None,
        gpu_name: str | None,
        gpu_vendor: str | None,
        vram_type: str | None,
        vram_gb: int | None,
        gpus_count: int,
    ) -> Hardware:
        gpu = await self._find_or_create_gpu(
            gpu_id, gpu_name, gpu_vendor, vram_type, vram_gb, gpus_count
        )
        hardware.update_gpu(gpu, gpus_count)
        await self._hardwares.save_hardware(hardware)
        return hardware

    async def update_cpu(
        self,
        hardware: Hardware,
        cpu_id: int | None,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
        cpus_count: int = 1,
    ) -> Hardware:
        cpu = await self._find_or_create_cpu(
            cpu_id, cpu_name, cpu_vendor, cores, frequency
        )
        hardware.update_cpu(cpu, cpus_count)
        await self._hardwares.save_hardware(hardware)
        return hardware

    async def update_storage(self, hardware: Hardware, storage_gb: int) -> Hardware:
        hardware.update_storage(storage_gb)
        await self._hardwares.save_hardware(hardware)
        return hardware

    async def update_ram(
        self,
        hardware: Hardware,
        ram_gb: int,
    ) -> Hardware:
        hardware.update_ram(ram_gb)
        await self._hardwares.save_hardware(hardware)
        return hardware

    async def delete_hardware(self, hardware_id: int) -> None:
        await self._hardwares.delete_hardware(hardware_id)

    async def delete_cpu(self, cpu_id: int) -> None:
        await self._hardwares.delete_cpu(cpu_id)

    async def delete_gpu(self, gpu_id: int) -> None:
        await self._hardwares.delete_gpu(gpu_id)
