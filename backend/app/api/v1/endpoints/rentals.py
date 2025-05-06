from fastapi import APIRouter, Depends

from app.api.v1.schemas.rental import CreateRental
from app.db.connector import ServicesFactory, get_services_factory
from app.models.rental import Rental
from app.services.rental_service import RentalService

router = APIRouter(prefix="/rentals", tags=["Rentals"])


async def get_rental_service(
    services: ServicesFactory = Depends(get_services_factory),
) -> RentalService:
    return services.get_rental_service()


@router.get("/")
async def get_rentals(
    rental_service: RentalService = Depends(get_rental_service),
) -> list[Rental]:
    return rental_service.get_rentals()


@router.get("/user/{user_id}")
async def get_rentals_by_user(
    user_id: int,
    rental_service: RentalService = Depends(get_rental_service),
) -> list[Rental]:
    return rental_service.get_rentals_by_user(user_id)


@router.post("/")
async def create_rental(
    rental: CreateRental,
    rental_service: RentalService = Depends(get_rental_service),
) -> Rental:
    return rental_service.create_rental(**rental.model_dump())


@router.patch("/{rental_id}")
async def extend_rental(
    rental_id: int, rental_service: RentalService = Depends(get_rental_service)
) -> Rental:
    return rental_service.extend_rental(rental_id)
