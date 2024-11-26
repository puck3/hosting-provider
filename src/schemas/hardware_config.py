from pydantic import BaseModel, PositiveFloat, PositiveInt

from src.schemas.base import default_str


class CPU(BaseModel):
    cpu_id: int | None
    cpu_name: default_str
    cpu_vendor: default_str
    cores: PositiveInt
    frequency: PositiveFloat


class GPU(BaseModel):
    gpu_id: int | None
    gpu_name: default_str
    vram_type: default_str
    vram_gb: PositiveInt


class HardwareConfigBase(BaseModel):
    cpus_count: PositiveInt
    gpus_count: PositiveInt
    storage_gb: PositiveInt
    ram_gb: PositiveInt
    bandwidth: PositiveInt


class HardwareConfigResponse(HardwareConfigBase):
    config_id: int
    cpu: CPU
    gpu: GPU


class HardwareConfigRequest(HardwareConfigBase):
    cpu_id: int
    gpu_id: int
