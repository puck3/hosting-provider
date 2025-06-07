from app.core.security import JWT
from app.db.redis.plan_cache import PlanCache
from app.db.redis.publisher import Publisher
from app.db.redis.token_repository import TokenRepository
from app.services.auth_service import AuthService
from app.services.hardware_service import HardwareService
from app.services.plan_service import PlanService
from app.services.rental_service import RentalService
from app.services.repositories_abc import RepositoriesFactoryABC
from app.services.server_service import ServerService
from app.services.user_service import UserService


class ServicesFactory:
    def __init__(
        self,
        repositories: RepositoriesFactoryABC,
        jwt_access: JWT,
        jwt_refresh: JWT,
        tokens: TokenRepository,
        plan_cache: PlanCache,
        publisher: Publisher,
    ) -> None:
        self._repositories = repositories
        self._jwt_access = jwt_access
        self._jwt_refresh = jwt_refresh
        self._tokens = tokens
        self._plan_cache = plan_cache
        self._publisher = publisher

    def get_user_service(self):
        return UserService(self._repositories)

    def get_hardware_service(self):
        return HardwareService(self._repositories)

    def get_plan_service(self):
        return PlanService(self._repositories, self._plan_cache)

    def get_server_service(self):
        return ServerService(self._repositories, publisher=self._publisher)

    def get_rental_service(self):
        return RentalService(self._repositories, publisher=self._publisher)

    def get_auth_service(self):
        return AuthService(
            repositories=self._repositories,
            jwt_access=self._jwt_access,
            jwt_refresh=self._jwt_refresh,
            tokens=self._tokens,
        )
