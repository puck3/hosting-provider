from src.services.repositories_abc import RepositoriesFactoryABC
from src.models.plan import BillingPeriod, Plan


class PlanService:
    def __init__(self, repositories: RepositoriesFactoryABC) -> None:
        self._plans = repositories.get_plan_repository()
        self._hardwares = repositories.get_hardware_repository()

    def add_plan(
        self,
        hardware_id: int,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
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
        )
        return plan

    def delete_plan(self, plan_id: int) -> None:
        self._plans.delete_plan(plan_id)

    def get_plans(self):
        return self._plans.get_plans()

    def get_available_plans_by_country(self, country: str) -> list[Plan]:
        return self._plans.get_available_plans_by_country(country)
