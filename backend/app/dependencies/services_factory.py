from typing import Annotated

from fastapi import Depends

from app.core.security import JWT
from app.db.redis.plan_cache import get_plan_cache
from app.db.redis.publisher import Publisher, get_publisher
from app.db.redis.token_repository import TokenRepository, get_token_repository
from app.dependencies.jwt import get_jwt_access, get_jwt_refresh
from app.dependencies.repositories_factory import get_repositories_factory
from app.services.factory import PlanCache, ServicesFactory
from app.services.repositories_abc import RepositoriesFactoryABC


def get_services_factory(
    repositories: Annotated[RepositoriesFactoryABC, Depends(get_repositories_factory)],
    jwt_access: Annotated[JWT, Depends(get_jwt_access)],
    jwt_refresh: Annotated[JWT, Depends(get_jwt_refresh)],
    tokens: Annotated[TokenRepository, Depends(get_token_repository)],
    plan_cache: Annotated[PlanCache, Depends(get_plan_cache)],
    publisher: Annotated[Publisher, Depends(get_publisher)],
) -> ServicesFactory:
    return ServicesFactory(
        repositories=repositories,
        jwt_access=jwt_access,
        jwt_refresh=jwt_refresh,
        tokens=tokens,
        plan_cache=plan_cache,
        publisher=publisher,
    )
