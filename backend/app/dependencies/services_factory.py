from typing import Annotated

from fastapi import Depends
from app.dependencies.repositories_factory import get_repositories_factory
from app.services.factory import ServicesFactory
from app.services.repositories_abc import RepositoriesFactoryABC


def get_services_factory(
    repositories: Annotated[
        RepositoriesFactoryABC, Depends(get_repositories_factory)
    ],
) -> ServicesFactory:
    return ServicesFactory(repositories)
