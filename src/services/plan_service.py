from src.models.hardware import Hardware
from src.models.user import User
from src.services.repositories_abc import PlanRepositoryABC
from src.models.plan import BillingPeriod, Plan


class PlanService:
    def __init__(self, plans: PlanRepositoryABC) -> None:
        self._plans = plans

    async def add_plan(
        self,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        name: str,
        description: str,
    ) -> Plan:
        plan = await self._plans.create_plan(
            hardware, price, billing_period, name, description
        )
        return plan

    async def update_price(self, plan: Plan, price: float) -> Plan:
        plan.update_price(price)
        await self._plans.save_plan(plan)
        return plan

    async def update_info(
        self, plan: Plan, name: str | None, description: str | None
    ) -> Plan:
        plan.update_info(name, description)
        if name is not None and description is not None:
            await self._plans.save_plan(plan)
        return plan

    async def delete_plan(self, plan_id: int) -> None:
        await self._plans.delete_plan(plan_id)

    async def get_plan_list(self, skip: int | None = None, limit: int | None = None):
        return await self._plans.get_plan_list(skip, limit)
