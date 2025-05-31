from src.models.hardware import CPU, GPU, Hardware
from src.utils.auth_client import Client


class HardwareService:
    def __init__(self, client: Client) -> None:
        self.client = client

    def get_hardwares(self) -> list[Hardware]:
        response = self.client.request("GET", "/hardwares")
        return [Hardware.model_validate(hardware) for hardware in response]

    def create_hardware(
        self,
        cpu_id: int,
        cpus_count: int,
        gpu_id: int | None,
        gpus_count: int,
        storage_tb: int,
        ram_gb: int,
        bandwidth_gbps: int,
    ) -> Hardware:
        body = {
            "cpu_id": cpu_id,
            "cpus_count": cpus_count,
            "gpu_id": gpu_id,
            "gpus_count": gpus_count,
            "storage_tb": storage_tb,
            "ram_gb": ram_gb,
            "bandwidth_gbps": bandwidth_gbps,
        }
        response = self.client.protected_request("POST", "/hardwares", json=body)
        return Hardware.model_validate(response)

    def delete_hardware(self, hardware_id: int) -> None:
        self.client.protected_request("DELETE", f"/hardwares/{hardware_id}")

    def get_cpus(self) -> list[CPU]:
        response = self.client.request("GET", "/hardwares/cpus")
        return [CPU.model_validate(cpu) for cpu in response]

    def add_cpu(self, cpu_name: str, cpu_vendor: str, cores: int, frequency: float) -> CPU:
        body = {
            "cpu_name": cpu_name,
            "cpu_vendor": cpu_vendor,
            "cores": cores,
            "frequency": frequency,
        }
        response = self.client.protected_request("POST", "/hardwares/cpus", json=body)
        return CPU.model_validate(response)

    def delete_cpu(self, cpu_id: int) -> None:
        self.client.protected_request("DELETE", f"/hardwares/cpus/{cpu_id}")

    def get_gpus(self) -> list[GPU]:
        response = self.client.request("GET", "/hardwares/gpus")
        return [GPU.model_validate(gpu) for gpu in response]

    def add_gpu(self, gpu_name: str, gpu_vendor: str, vram_type: str, vram_gb: int) -> GPU:
        body = {
            "gpu_name": gpu_name,
            "gpu_vendor": gpu_vendor,
            "vram_type": vram_type,
            "vram_gb": vram_gb,
        }
        response = self.client.protected_request("POST", "/hardwares/gpus", json=body)
        return GPU.model_validate(response)

    def delete_gpu(self, gpu_id: int) -> None:
        self.client.protected_request("DELETE", f"/hardwares/gpus/{gpu_id}")
