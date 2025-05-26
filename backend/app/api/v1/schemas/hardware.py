from pydantic import BaseModel


class CreateHardware(BaseModel):
    cpu_id: int
    cpus_count: int
    gpu_id: int | None
    gpus_count: int
    storage_tb: int
    ram_gb: int
    bandwidth_gbps: int


class CreateCPU(BaseModel):
    cpu_name: str
    cpu_vendor: str
    cores: int
    frequency: float


class CreateGPU(BaseModel):
    gpu_name: str
    gpu_vendor: str
    vram_type: str
    vram_gb: int
