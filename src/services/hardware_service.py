from src.models.hardware import Hardware, CPU, GPU
from src.services.repositories_abc import RepositoriesFactoryABC


class HardwareService:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._hardwares = repositories.get_hardware_repository()

    async def add_cpu(
        self, cpu_name: str, cpu_vendor: str, cores: int, frequency: float
    ) -> GPU:
        if await self._hardwares.get_cpu_by_name(cpu_name):
            raise ValueError("CPU is already added.")

        cpu = await self._hardwares.create_cpu(cpu_name, cpu_vendor, cores, frequency)
        return cpu

    async def get_cpus(self) -> list[CPU]:
        return await self._hardwares.get_cpus()

    async def delete_cpu(self, cpu_id: int) -> None:
        await self._hardwares.delete_cpu(cpu_id)

    async def add_gpu(
        self, gpu_name: str, gpu_vendor: str, vram_type: str, vram_gb: int
    ) -> GPU:
        if await self._hardwares.get_gpu_by_name(gpu_name):
            raise ValueError("GPU is already added.")

        gpu = await self._hardwares.create_gpu(gpu_name, gpu_vendor, vram_type, vram_gb)
        return gpu

    async def get_gpus(self) -> list[GPU]:
        return await self._hardwares.get_gpus()

    async def delete_gpu(self, gpu_id: int) -> None:
        await self._hardwares.delete_gpu(gpu_id)

    async def create_hardware(
        self,
        cpu_id: int,
        cpus_count: int,
        gpu_id: int | None,
        gpus_count: int,
        storage_gb: int,
        ram_gb: int,
        bandwidth_mbps: int,
    ) -> Hardware:
        if (cpu := await self._hardwares.get_cpu_by_id(cpu_id)) is None:
            raise ValueError("CPU not found")

        if gpu_id is not None and gpus_count == 0:
            raise ValueError("GPUs count must be positive to find gpu")

        gpu = (
            await self._hardwares.get_gpu_by_id(gpu_id) if gpu_id is not None else None
        )
        if gpu is None and gpus_count > 0:
            raise ValueError("GPU not found")

        hardware = await self._hardwares.create_hardware(
            cpu, cpus_count, storage_gb, ram_gb, bandwidth_mbps, gpu, gpus_count
        )
        return hardware

    async def get_hardwares(self) -> list[Hardware]:
        return await self._hardwares.get_hardwares()

    async def delete_hardware(self, hardware_id: int) -> None:
        await self._hardwares.delete_hardware(hardware_id)
