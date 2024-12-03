from asyncpg import Record
from src.models.hardware import Hardware
from src.models.plan import BillingPeriod, Plan
from src.services.repositories_abc import PlanRepositoryABC
from src.db.base import BaseRepository
from src.db.hardware_repository import HardwareRepository


class PlanRepository(BaseRepository, PlanRepositoryABC):
    async def create_plan(
        self,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> Plan:
        query = """
            INSERT INTO plans (
                hardware_id, price, billing_period, plan_name, plan_description
            ) 
            VALUES (
                $1, $2, $3, $4, $5
            )
            RETURNING plan_id;
        """
        hardware_id = hardware.hardware_id
        async with self._get_connection() as conn:
            plan_id = await conn.fetchval(
                query, hardware_id, price, billing_period, plan_name, plan_description
            )

        plan = Plan(
            plan_id=plan_id,
            hardware=hardware,
            price=price,
            billing_period=billing_period,
            plan_name=plan_name,
            plan_description=plan_description,
        )
        return plan

    async def delete_plan(self, plan_id: int) -> None:
        query = """
            DELETE FROM plans
            WHERE plan_id = $1;
        """
        async with self._get_connection() as conn:
            await conn.execute(query, plan_id)

    @staticmethod
    def get_plan_from_record(record: Record | None) -> Plan | None:
        if record is None:
            return None
        else:
            plan_data = {
                key: value
                for key, value in record.items()
                if key in Plan.model_fields.items()
            }
            plan_data["hardware"] = HardwareRepository.get_hardware_from_record(record)
            return Plan(**plan_data)

    async def get_plan_by_id(self, plan_id: int) -> Plan | None:
        query = """
            SELECT *
            FROM
                plans 
                LEFT JOIN extended_hardwares using(hardware_id)
            WHERE
                plan_id = $1
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, plan_id)

        return self.get_plan_from_record(result)

    async def get_plan_by_name(self, plan_name: str) -> Plan | None:
        query = """
            SELECT *
            FROM
                plans
                LEFT JOIN extended_hardwares using(hardware_id)
            WHERE
                plan_name = $1
        """
        async with self._get_connection() as conn:
            result = await conn.fetchrow(query, plan_name)

        return self.get_plan_from_record(result)

    async def get_plans(self) -> list[Plan]:
        query = """
            SELECT *
            FROM
                plans
                LEFT JOIN extended_hardwares using(hardware_id)
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query)

        return [self.get_plan_from_record(record) for record in result]

    async def get_available_plans_by_country(self, country: str) -> list[Plan]:
        query = """
            SELECT *
            FROM available_plans_with_countries
            WHERE country = $1;
        """
        async with self._get_connection() as conn:
            result = await conn.fetch(query, country)

        return [self.get_plan_from_record(record) for record in result]
