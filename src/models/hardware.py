from src.models.base import BaseModel


class GPU(BaseModel):
    def __init__(
        self,
        gpu_id: int,
        gpu_name: str,
        gpu_vendor: str,
        vram_type: str,
        vram_gb: int,
        **kwargs,
    ) -> None:
        self._set_id(gpu_id)
        self._gpu_name = gpu_name
        self._gpu_vendor = gpu_vendor
        self._vram_type = vram_type
        self._vram_gb = vram_gb


class CPU(BaseModel):
    def __init__(
        self,
        cpu_id: int,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
        **kwargs,
    ) -> None:
        self._set_id(cpu_id)
        self._cpu_name = cpu_name
        self._cpu_vendor = cpu_vendor
        self._cores = cores
        self._frequency = frequency


class Hardware(BaseModel):
    def __init__(
        self,
        hardware_id: int,
        cpu: CPU,
        cpus_count: int,
        storage_gb: int,
        ram_gb: int,
        bandwidth_mbps: int,
        gpu: GPU | None = None,
        gpus_count: int = 0,
        **kwargs,
    ):
        self._set_id(hardware_id)
        self._cpu = cpu
        self._cpus_count = cpus_count
        self._gpu = gpu
        self._gpus_count = gpus_count
        self._storage_gb = storage_gb
        self._ram_gb = ram_gb
        self._bandwidth_mbps = bandwidth_mbps

    def update_cpu(self, cpu: CPU, cpus_count: int) -> None:
        self._cpu = cpu
        self._cpus_count = cpus_count

    def update_gpu(self, gpu: GPU, gpus_count: int) -> None:
        self._gpu = gpu
        self._gpus_count = gpus_count

    def update_storage(self, storage_gb: int) -> None:
        self._storage_gb = storage_gb

    def update_ram(self, ram_gb: int) -> None:
        self._ram_gb = ram_gb
