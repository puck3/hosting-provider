from psycopg2.pool import SimpleConnectionPool

from app.db.hardware_repository import HardwareRepository
from app.db.plan_repository import PlanRepository
from app.db.rental_repository import RentalRepository
from app.db.server_repository import ServerRepository
from app.db.user_repository import UserRepository
from app.services.factory import RepositoriesFactoryABC


class RepositoriesFactory(RepositoriesFactoryABC):
    def __init__(self, pool: SimpleConnectionPool):
        self._pool = pool

    def get_user_repository(self) -> UserRepository:
        return UserRepository(self._pool)

    def get_hardware_repository(self) -> HardwareRepository:
        return HardwareRepository(self._pool)

    def get_plan_repository(self) -> PlanRepository:
        return PlanRepository(self._pool)

    def get_server_repository(self) -> ServerRepository:
        return ServerRepository(self._pool)

    def get_rental_repository(self) -> RentalRepository:
        return RentalRepository(self._pool)
