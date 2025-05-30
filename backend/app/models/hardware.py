from pydantic import BaseModel


class GPU(BaseModel):
    gpu_id: int
    gpu_name: str
    gpu_vendor: str
    vram_type: str
    vram_gb: int


class CPU(BaseModel):
    cpu_id: int
    cpu_name: str
    cpu_vendor: str
    cores: int
    frequency: float


class Hardware(BaseModel):
    hardware_id: int
    cpu: CPU
    cpus_count: int
    gpu: GPU | None
    gpus_count: int
    storage_tb: int
    ram_gb: int
    bandwidth_gbps: int
