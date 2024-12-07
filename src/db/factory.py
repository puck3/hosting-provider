from psycopg2.pool import SimpleConnectionPool
from src.db.hardware_repository import HardwareRepository
from src.db.plan_repository import PlanRepository
from src.db.rental_repository import RentalRepository
from src.db.server_repository import ServerRepository
from src.db.user_repository import UserRepository


class RepositoriesFactory:
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
