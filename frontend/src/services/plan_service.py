from src.models.plan import BillingPeriod, Plan
from src.utils.client import Client


class PlanService:
    def __init__(self, client: Client):
        self.client = client

    def get_plans(self) -> list[Plan]:
        response = self.client.request("GET", "/plans")
        return [Plan.model_validate(plan) for plan in response]

    def get_available_plans_by_country(self, country: str) -> list[Plan]:
        response = self.client.request("GET", f"/plans/available/{country}")
        return [Plan.model_validate(plan) for plan in response]

    def add_plan(
        self,
        hardware_id: int,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str | None = None,
    ) -> Plan:
        body = {
            "hardware_id": hardware_id,
            "price": price,
            "billing_period": billing_period.value,
            "plan_name": plan_name,
            "plan_description": plan_description,
        }

        response = self.client.protected_request("POST", "/plans", json=body)
        return Plan.model_validate(response)

    def delete_plan(self, plan_id: int) -> None:
        self.client.protected_request("DELETE", f"/plans/{plan_id}")
