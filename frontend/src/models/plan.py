from enum import Enum

from pydantic import BaseModel

from src.models.hardware import Hardware


class BillingPeriod(str, Enum):
    hourly = "hourly"
    daily = "daily"
    monthly = "monthly"


class Plan(BaseModel):
    plan_id: int
    hardware: Hardware
    price: float
    billing_period: BillingPeriod
    plan_name: str
