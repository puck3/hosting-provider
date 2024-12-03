from datetime import datetime, timedelta

from asyncpg import Record
from src.db.base import BaseRepository
from src.db.plan_repository import PlanRepository
from src.db.server_repository import ServerRepository
from src.models.plan import BillingPeriod, Plan
from src.models.rental import Rental
from src.models.server import Server
from src.models.user import User
from src.services.repositories_abc import RentalRepositoryABC


class RentalRepository(BaseRepository, RentalRepositoryABC):
    async def create_rental(self, user: User, server: Server, plan: Plan) -> Rental:
        query = """
            INSERT INTO rentals (
                user_id, server_id, plan_id, start_at, end_at, update_at
            )
            VALUES (
                $1, $2, $3, $4, $5, $4
            )
            RETURNING rental_id,
        """
        start_at = end_at = datetime.now()
        match plan.billing_period:
            case BillingPeriod.hourly:
                end_at += timedelta(hours=1)
            case BillingPeriod.daily:
                end_at += timedelta(days=1)
            case BillingPeriod.monthly:
                end_at += timedelta(days=30)

        async with self._get_connection() as conn:
            rental_id = await conn.fetchval(
                query, user.user_id, server.server_id, plan.plan_id, start_at, end_at
            )

        rental = Rental(
            rental_id=rental_id,
            user=user,
            server=server,
            plan=plan,
            start_at=start_at,
            end_at=end_at,
            update_at=start_at,
        )
        return rental

    async def save_rental(self, rental: Rental) -> None:
        query = """
            UPDATE rentals
            SET server = $1, plan = $2, end_at = $3
            WHERE rental_id = $4;
        """
        async with self._get_connection() as conn:
            await conn.execute(
                query,
                rental.server.server_id,
                rental.plan.plan_id,
                rental.end_at,
                rental.rental_id,
            )

    @staticmethod
    def get_rental_from_record(record: Record | None) -> Rental | None:
        if record is None:
            return None
        else:
            rental_data = {
                key: value
                for key, value in record.items()
                if key in Rental.model_fields.keys()
            }
            user_data = {
                key: value
                for key, value in record.items()
                if key in User.model_fields.keys()
            }
            rental_data["user"] = User(**user_data)
            rental_data["server"] = ServerRepository.get_server_from_record(record)
            rental_data["plan"] = PlanRepository.get_plan_from_record(record)
            return Rental(**rental_data)

    async def get_rental_by_id(self, rental_id: int) -> Rental | None:
        query = """
            SELECT *
            FROM extended_rentals
            WHERE rental_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, rental_id)

        return self.get_rental_from_record(result)

    async def get_rentals(self) -> list[Rental]:
        query = """
            SELECT *
            FROM extended_rentals;
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self.get_rental_from_record(record) for record in result]

    async def get_rentals_by_user(self, user_id: int) -> list[Rental]:
        query = """
            SELECT *
            FROM extended_rentals
            WHERE user_id = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query, user_id)

        return [self.get_rental_from_record(record) for record in result]
