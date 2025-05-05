from enum import Enum
from pydantic import BaseModel
from app.models.hardware import Hardware


class BillingPeriod(str, Enum):
    hourly = "час"
    daily = "сутки"
    monthly = "месяц"


class Plan(BaseModel):
    plan_id: int
    hardware: Hardware
    price: float
    billing_period: BillingPeriod
    plan_name: str
