from src.services.repositories_abc import RepositoriesFactoryABC
from src.models.plan import BillingPeriod, Plan


class PlanService:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._plans = repositories.get_plan_repository()
        self._hardwares = repositories.get_hardware_repository()

    async def add_plan(
        self,
        hardware_id: int,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> Plan:
        if self._plans.get_plan_by_name(plan_name) is not None:
            raise ValueError("Plan already exists")

        if (hardware := await self._hardwares.get_hardware_by_id(hardware_id)) is None:
            raise ValueError("Hardware not found.")

        plan = await self._plans.create_plan(
            hardware, price, billing_period, plan_name, plan_description
        )
        return plan

    async def delete_plan(self, plan_id: int) -> None:
        await self._plans.delete_plan(plan_id)

    async def get_plans(self):
        return await self._plans.get_plans()

    async def get_available_plans_by_country(self, country: str) -> list[Plan]:
        return await self._plans.get_available_plans_by_country(self, country)
