from src.models.rental import Rental
from src.utils.auth_client import Client


class RentalService:
    def __init__(self, client: Client) -> None:
        self.client = client

    def get_rentals(self) -> list[Rental]:
        response = self.client.protected_request("GET", "/rentals")
        return [Rental.model_validate(rental) for rental in response]

    def get_rentals_by_user(self, user_id: int) -> list[Rental]:
        response = self.client.protected_request("GET", f"/rentals/user/{user_id}")
        return [Rental.model_validate(rental) for rental in response]

    def create_rental(self, plan_id: int, country: str) -> Rental:
        body = {
            "plan_id": plan_id,
            "country": country,
        }
        response = self.client.protected_request("POST", "/rentals", json=body)
        return Rental.model_validate(response)

    def extend_rental(self, rental_id: int) -> Rental:
        response = self.client.protected_request("PATCH", f"/rentals/{rental_id}/extend")
        return Rental.model_validate(response)
