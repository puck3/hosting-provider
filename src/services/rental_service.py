from datetime import datetime
from src.models.rental import Rental
from src.services.repositories_abc import RepositoriesFactoryABC


class RentalService:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._rentals = repositories.get_rental_repository()
        self._users = repositories.get_user_repository()
        self._servers = repositories.get_server_repository()
        self._plans = repositories.get_plan_repository()

    def create_rental(self, user_id: int, plan_id: int, country: str) -> Rental:
        if (user := self._users.get_user_by_id(user_id)) is None:
            raise ValueError("User not found.")

        if (plan := self._plans.get_plan_by_id(plan_id)) is None:
            raise ValueError("Plan not found.")

        server_id = self._servers.reserve_server(plan.hardware.hardware_id, country)

        if (server := self._servers.get_server_by_id(server_id)) is None:
            raise ValueError("Server not found.")

        rental = self._rentals.create_rental(
            user, server, plan.price, plan.billing_period
        )
        return rental

    def get_rentals(self) -> list[Rental]:
        return self._rentals.get_rentals()

    def get_rentals_by_user(self, user_id: int) -> list[Rental]:
        return self._rentals.get_rentals_by_user(user_id)

    def extend_rental(self, rental_id: int):
        if (rental := self._rentals.get_rental_by_id(rental_id)) is None:
            raise ValueError("Rental not found.")

        if rental.end_at < datetime.now():
            raise ValueError("Rental already ended.")

        rental.extend()
        self._rentals.save_rental(rental)
