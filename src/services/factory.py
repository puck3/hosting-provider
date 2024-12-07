from src.services.hardware_service import HardwareService
from src.services.plan_service import PlanService
from src.services.rental_service import RentalService
from src.services.repositories_abc import RepositoriesFactoryABC
from src.services.server_service import ServerService
from src.services.user_service import UserService


class ServicesFactory:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._repositories = repositories

    def get_user_service(self):
        return UserService(self._repositories)

    def get_hardware_service(self):
        return HardwareService(self._repositories)

    def get_plan_service(self):
        return PlanService(self._repositories)

    def get_server_service(self):
        return ServerService(self._repositories)

    def get_rental_service(self):
        return RentalService(self._repositories)
