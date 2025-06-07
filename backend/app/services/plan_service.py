from app.db.redis.plan_cache import PlanCache
from app.models.plan import BillingPeriod, Plan
from app.services.repositories_abc import RepositoriesFactoryABC
from app.utils.logger import logger


class PlanService:
    def __init__(self, repositories: RepositoriesFactoryABC, cache: PlanCache) -> None:
        self._plans = repositories.get_plan_repository()
        self._hardwares = repositories.get_hardware_repository()
        self._cache = cache

    def add_plan(
        self,
        hardware_id: int,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> Plan:
        if self._plans.get_plan_by_name(plan_name) is not None:
            raise ValueError("Plan already exists")

        if (hardware := self._hardwares.get_hardware_by_id(hardware_id)) is None:
            raise ValueError("Hardware not found.")

        plan = self._plans.create_plan(
            hardware,
            price,
            billing_period,
            plan_name,
            plan_description,
        )
        return plan

    def delete_plan(self, plan_id: int) -> None:
        self._plans.delete_plan(plan_id)

    def get_plans(self):
        return self._plans.get_plans()

    async def get_available_plans_by_country(self, country: str) -> list[Plan]:
        if plans := await self._cache.get_cached_tariffs_region(country):
            logger.info(f"Get plans from cache: {len(plans)}")
        else:
            plans = self._plans.get_available_plans_by_country(country)
            logger.info(f"Get plans from database: {len(plans)}")
            await self._cache.cache_tariffs_region(country, [p.model_dump() for p in plans])
        return self._plans.get_available_plans_by_country(country)
