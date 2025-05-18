from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.v1.schemas.rental import CreateRental
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.rental import Rental
from app.models.user import Role
from app.services.rental_service import RentalService
from app.services.factory import ServicesFactory

router = APIRouter(prefix="/rentals", tags=["Rentals"])


async def get_rental_service(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> RentalService:
    return services.get_rental_service()


@router.get("/")
async def get_rentals(
    rental_service: Annotated[RentalService, Depends(get_rental_service)],
) -> list[Rental]:
    return rental_service.get_rentals()


@router.get("/user/{user_id}")
async def get_rentals_by_user(
    user_id: int,
    rental_service: Annotated[RentalService, Depends(get_rental_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> list[Rental]:
    if actor.role != Role.admin and actor.user_id != user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can get rentals by user.",
        )
    return rental_service.get_rentals_by_user(user_id)


@router.post("/")
async def create_rental(
    rental: CreateRental,
    rental_service: Annotated[RentalService, Depends(get_rental_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Rental:
    return rental_service.create_rental(actor.user_id, **rental.model_dump())


@router.patch("/{rental_id}")
async def extend_rental(
    rental_id: int,
    rental_service: Annotated[RentalService, Depends(get_rental_service)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Rental:
    return rental_service.extend_rental(actor.user_id, rental_id)
