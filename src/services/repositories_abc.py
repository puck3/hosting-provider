from abc import ABC, abstractmethod
from datetime import date

from src.models.hardware import CPU, GPU, Hardware
from src.models.plan import BillingPeriod, Plan
from src.models.rental import Rental
from src.models.server import Datacenter, Server, Status
from src.models.user import User, Role


class UserRepositoryABC(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User | None: ...

    @abstractmethod
    async def create_user(
        self,
        email: str,
        login: str,
        password_hash: str,
        role: Role = Role.user,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> User: ...

    @abstractmethod
    async def save_user(self, user: User) -> None: ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> None: ...


class HardwareRepositoryABC(ABC):
    @abstractmethod
    async def get_hardware_by_id(self, hardware_id: int) -> Hardware | None: ...

    @abstractmethod
    async def get_cpu_by_name(self, cpu_name: str) -> CPU | None: ...

    @abstractmethod
    async def get_gpu_by_name(self, gpu_name: str) -> GPU | None: ...

    @abstractmethod
    async def get_hardware_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Hardware]: ...

    @abstractmethod
    async def get_cpu_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[CPU]: ...

    @abstractmethod
    async def get_gpu_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[GPU]: ...

    @abstractmethod
    async def create_cpu(
        self,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
    ) -> CPU: ...

    @abstractmethod
    async def create_gpu(
        self,
        gpu_name: str,
        gpu_vendor: str,
        vram_type: str,
        vram_gb: int,
    ) -> GPU: ...

    @abstractmethod
    async def create_hardware(
        self,
        cpu: CPU,
        cpus_count: int,
        storage_gb: int,
        ram_gb: int,
        bandwidth_mbps: int,
        gpu: GPU | None = None,
        gpus_count: int = 0,
    ) -> Hardware: ...

    @abstractmethod
    async def save_hardware(self, hardware: Hardware) -> None: ...

    @abstractmethod
    async def delete_hardware(self, hardware_id: int) -> None: ...

    @abstractmethod
    async def delete_cpu(self, cpu_id: int) -> None: ...

    @abstractmethod
    async def delete_gpu(self, gpu_id: int) -> None: ...


class PlanRepositoryABC(ABC):
    @abstractmethod
    async def get_plan_by_id(self, plan_id: int) -> Plan | None: ...

    @abstractmethod
    async def get_plan_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Plan]: ...

    @abstractmethod
    async def create_plan(
        self,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        name: str,
        description: str,
    ) -> Plan: ...

    @abstractmethod
    async def save_plan(self, plan: Plan) -> None: ...

    @abstractmethod
    async def delete_plan(self, plan_id: int) -> None: ...


class ServerRepositoryABC(ABC):
    @abstractmethod
    async def create_server(
        self,
        datacenter: Datacenter,
        hardware: Hardware,
        status: Status,
        operating_system: str,
    ) -> Server: ...

    @abstractmethod
    async def create_datacenter(
        self,
        name: str,
        country: str,
        city: str,
    ) -> Datacenter: ...

    @abstractmethod
    async def save_server(self, server: Server) -> None: ...

    @abstractmethod
    async def delete_server(self, server_id: int) -> None: ...

    @abstractmethod
    async def delete_datacenter(self, datacenter_id: int) -> None: ...

    @abstractmethod
    async def get_datacenter_by_name(
        self, datacenter_name: str
    ) -> Datacenter | None: ...

    @abstractmethod
    async def find_inactive_server(
        self, hardware: Hardware, country: str | None = None, city: str | None = None
    ) -> Server | None: ...

    @abstractmethod
    async def get_server_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Server]: ...


class RentalRepositoryABC(ABC):
    @abstractmethod
    async def create_rental(self, user: User, server: Server, plan: Plan) -> Rental: ...

    @abstractmethod
    async def save_rental(self, rental: Rental) -> None: ...

    @abstractmethod
    async def get_rental_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Rental]: ...
