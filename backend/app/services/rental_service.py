from datetime import datetime

from app.db.redis.publisher import Publisher
from app.models.rental import Rental
from app.services.repositories_abc import RepositoriesFactoryABC


class RentalService:
    def __init__(self, repositories: RepositoriesFactoryABC, publisher: Publisher) -> None:
        self._rentals = repositories.get_rental_repository()
        self._users = repositories.get_user_repository()
        self._servers = repositories.get_server_repository()
        self._plans = repositories.get_plan_repository()
        self._publisher = publisher

    async def create_rental(self, user_id: int, plan_id: int, country: str) -> Rental:
        if (user := self._users.get_user_by_id(user_id)) is None:
            raise ValueError("User not found.")

        if (plan := self._plans.get_plan_by_id(plan_id)) is None:
            raise ValueError("Plan not found.")

        server_id = self._servers.reserve_server(plan.hardware.hardware_id, country)

        if (server := self._servers.get_server_by_id(server_id)) is None:
            raise ValueError("Server not found.")

        rental = self._rentals.create_rental(user, server, plan.price, plan.billing_period)

        await self._publisher.publish_event(
            "rental_created", {"rental_id": rental.rental_id, "user_id": user_id, "server_id": server_id}
        )
        return rental

    def get_rentals(self) -> list[Rental]:
        return self._rentals.get_rentals()

    def get_rentals_by_user(self, user_id: int) -> list[Rental]:
        return self._rentals.get_rentals_by_user(user_id)

    def extend_rental(self, user_id: int, rental_id: int) -> Rental:
        if (rental := self._rentals.get_rental_by_id(rental_id)) is None:
            raise ValueError("Rental not found.")

        if rental.user.user_id != user_id:
            raise ValueError("Rental does not belong to user.")

        if rental.end_at < datetime.now():
            raise ValueError("Rental already ended.")

        rental.extend()
        self._rentals.save_rental(rental)
        return rental
