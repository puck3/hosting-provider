from datetime import datetime
from src.models.plan import BillingPeriod, Plan
from src.models.rental import Rental
from src.models.user import User
from src.services.repositories_abc import RentalRepositoryABC, ServerRepositoryABC


class RentalService:
    def __init__(
        self, rentals: RentalRepositoryABC, servers: ServerRepositoryABC
    ) -> None:
        self._rentals = rentals
        self._servers = servers

    async def create_rental(
        self,
        user: User,
        plan: Plan,
        country: str | None = None,
        city: str | None = None,
    ) -> Rental:
        hardware = plan.dict()["hardware"]
        server = await self._servers.find_inactive_server(hardware, country, city)
        if server is None:
            raise ValueError("Available server not found.")
        return await self._rentals.create_rental(user, server, plan)

    async def update_end_time(self, rental: Rental) -> Rental:
        end_at: datetime = rental.dict()["end_at"]
        if end_at < datetime.now():
            raise ValueError("Current rental is already ended.")
        rental.update_end_time()
        await self._rentals.save_rental(rental)
        return rental

    async def get_rentals_list(
        self, skip: int | None = None, limit: int | None = None
    ) -> list[Rental]:
        return self._rentals.get_rental_list(skip, limit)
