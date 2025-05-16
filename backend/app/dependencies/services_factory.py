from typing import Annotated

from fastapi import Depends
from app.core.security import JWT
from app.dependencies.jwt import get_jwt_access, get_jwt_refresh
from app.dependencies.repositories_factory import get_repositories_factory
from app.services.factory import ServicesFactory
from app.services.repositories_abc import RepositoriesFactoryABC


def get_services_factory(
    repositories: Annotated[
        RepositoriesFactoryABC, Depends(get_repositories_factory)
    ],
    jwt_access: Annotated[JWT, get_jwt_access],
    jwt_refresh: Annotated[JWT, get_jwt_refresh],
) -> ServicesFactory:
    return ServicesFactory(repositories, jwt_access, jwt_refresh)
