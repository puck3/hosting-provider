from enum import Enum

from src.models.base import BaseModel
from src.models.hardware import Hardware


class BillingPeriod(str, Enum):
    hourly = "hourly"
    daily = "daily"
    monthly = "monthly"


class Plan(BaseModel):
    def __init__(
        self,
        plan_id: int,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> None:
        self._set_id(plan_id)
        self._hardware = hardware
        self._price = price
        self._billing_period = billing_period
        self._plan_name = plan_name
        self._plan_description = plan_description

    def update_price(self, price: float):
        self._price = price

    def update_info(self, name: str | None = None, plan_description: str | None = None):
        if name is not None:
            self._plan_name = name
        if plan_description is not None:
            self._plan_description = plan_description
