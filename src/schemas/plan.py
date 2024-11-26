from enum import Enum
from pydantic import BaseModel, PositiveFloat

from src.core.constants import default_str
from src.schemas.hardware_config import HardwareConfigResponse


class BillingPeriod(str, Enum):
    hourly = "hourly"
    daily = "daily"
    monthly = "monthly"


class PlanBase(BaseModel):
    price: PositiveFloat
    billing_period: BillingPeriod
    name: default_str
    description: str


class PlanResponse(PlanBase):
    plan_id: int
    config: HardwareConfigResponse


class PlanRequest(PlanBase):
    config_id: int
