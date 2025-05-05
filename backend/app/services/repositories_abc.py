from abc import ABC, abstractmethod
from datetime import date

from app.models.hardware import CPU, GPU, Hardware
from app.models.plan import BillingPeriod, Plan
from app.models.rental import Rental
from app.models.server import Datacenter, Server, Status
from app.models.user import User, Role


class UserRepositoryABC(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_user_by_login(self, login: str) -> User | None: ...

    @abstractmethod
    def get_users(self) -> list[User]: ...

    @abstractmethod
    def create_user(
        self,
        email: str,
        login: str,
        password_hash: str,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
        role: Role = Role.user,
    ) -> User: ...

    @abstractmethod
    def save_user(self, user: User) -> None: ...

    @abstractmethod
    def delete_user(self, user_id: int) -> None: ...


class HardwareRepositoryABC(ABC):
    @abstractmethod
    def get_cpu_by_id(self, cpu_id: int) -> CPU | None: ...

    @abstractmethod
    def get_cpu_by_name(self, cpu_name: str) -> CPU | None: ...

    @abstractmethod
    def get_cpus(self) -> list[CPU]: ...

    @abstractmethod
    def create_cpu(
        self,
        cpu_name: str,
        cpu_vendor: str,
        cores: int,
        frequency: float,
    ) -> CPU: ...

    @abstractmethod
    def delete_cpu(self, cpu_id: int) -> None: ...

    @abstractmethod
    def get_gpu_by_id(self, gpu_id: int) -> GPU | None: ...

    @abstractmethod
    def get_gpu_by_name(self, gpu_name: str) -> GPU | None: ...

    @abstractmethod
    def get_gpus(self) -> list[GPU]: ...

    @abstractmethod
    def create_gpu(
        self,
        gpu_name: str,
        gpu_vendor: str,
        vram_type: str,
        vram_gb: int,
    ) -> GPU: ...

    @abstractmethod
    def delete_gpu(self, gpu_id: int) -> None: ...

    @abstractmethod
    def get_hardware_by_id(self, hardware_id: int) -> Hardware | None: ...

    @abstractmethod
    def get_hardwares(self) -> list[Hardware]: ...

    @abstractmethod
    def create_hardware(
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
    def delete_hardware(self, hardware_id: int) -> None: ...


class PlanRepositoryABC(ABC):
    @abstractmethod
    def get_plan_by_id(self, plan_id: int) -> Plan | None: ...

    @abstractmethod
    def get_plan_by_name(self, plan_name: str) -> Plan | None: ...

    @abstractmethod
    def get_plans(self) -> list[Plan]: ...

    @abstractmethod
    def get_available_plans_by_country(self, country: str) -> list[Plan]: ...

    @abstractmethod
    def create_plan(
        self,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> Plan: ...

    @abstractmethod
    def delete_plan(self, plan_id: int) -> None: ...


class ServerRepositoryABC(ABC):
    @abstractmethod
    def create_datacenter(
        self,
        datacenter_name: str,
        country: str,
        city: str,
    ) -> Datacenter: ...

    @abstractmethod
    def delete_datacenter(self, datacenter_id: int) -> None: ...

    @abstractmethod
    def get_datacenter_by_id(self, datacenter_id: int) -> Datacenter | None: ...

    @abstractmethod
    def get_datacenter_by_name(
        self, datacenter_name: str
    ) -> Datacenter | None: ...

    @abstractmethod
    def get_datacenters(self) -> list[Datacenter]: ...

    @abstractmethod
    def create_server(
        self,
        datacenter: Datacenter,
        hardware: Hardware,
        status: Status,
        operating_system: str,
    ) -> Server: ...

    @abstractmethod
    def save_server(self, server: Server) -> None: ...

    @abstractmethod
    def delete_server(self, server_id: int) -> None: ...

    @abstractmethod
    def get_server_by_id(self, server_id: int) -> Server | None: ...

    @abstractmethod
    def reserve_server(self, hardware_id: int, country: str) -> int: ...

    @abstractmethod
    def get_servers(self) -> list[Server]: ...

    @abstractmethod
    def release_servers(self) -> None: ...

    @abstractmethod
    def fix_servers_status(self) -> None: ...


class RentalRepositoryABC(ABC):
    @abstractmethod
    def create_rental(
        self,
        user: User,
        server: Server,
        price: float,
        billing_period: BillingPeriod,
    ) -> Rental: ...

    @abstractmethod
    def save_rental(self, rental: Rental) -> None: ...

    @abstractmethod
    def get_rental_by_id(self, rental_id: int) -> Rental | None: ...

    @abstractmethod
    def get_rentals(self) -> list[Rental]: ...

    @abstractmethod
    def get_rentals_by_user(self, user_id: int) -> list[Rental]: ...


class RepositoriesFactoryABC(ABC):
    @abstractmethod
    def get_user_repository(self) -> UserRepositoryABC: ...

    @abstractmethod
    def get_hardware_repository(self) -> HardwareRepositoryABC: ...

    @abstractmethod
    def get_plan_repository(self) -> PlanRepositoryABC: ...

    @abstractmethod
    def get_server_repository(self) -> ServerRepositoryABC: ...

    @abstractmethod
    def get_rental_repository(self) -> RentalRepositoryABC: ...
