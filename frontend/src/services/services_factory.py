from src.services.hardware_service import HardwareService
from src.services.plan_service import PlanService
from src.services.rental_service import RentalService
from src.services.server_service import ServerService
from src.services.user_service import UserService
from src.utils.client import Client


class ServicesFactory:
    @staticmethod
    def get_user_service():
        return UserService(Client())

    @staticmethod
    def get_hardware_service():
        return HardwareService(Client())

    @staticmethod
    def get_plan_service():
        return PlanService(Client())

    @staticmethod
    def get_server_service():
        return ServerService(Client())

    @staticmethod
    def get_rental_service():
        return RentalService(Client())
