from src.models.hardware import CPU, GPU, Hardware
from src.models.server import Datacenter
from src.utils.hardware_info import get_hardware_info


class KeyIdMap:
    map: dict[str, int]

    def list_keys(self) -> list[str]:
        return list(self.map.keys())

    def get(self, key: str) -> int:
        return self.map[key]


class CPUKeyIdMap(KeyIdMap):
    def __init__(self, cpus: list[CPU]) -> None:
        self.map = {cpu.cpu_name: cpu.cpu_id for cpu in cpus}


class GPUKeyIdMap(KeyIdMap):
    def __init__(self, gpus: list[GPU]) -> None:
        self.map = {gpu.gpu_name: gpu.gpu_id for gpu in gpus}


class HardwareKeyIdMap(KeyIdMap):
    def __init__(self, hardwares: list[Hardware]) -> None:
        self.map = {get_hardware_info(hardware): hardware.hardware_id for hardware in hardwares}


class DatacenterKeyIdMap(KeyIdMap):
    def __init__(self, datacenters: list[Datacenter]) -> None:
        self.map = {datacenter.datacenter_name: datacenter.datacenter_id for datacenter in datacenters}
