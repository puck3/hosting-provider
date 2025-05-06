from pydantic import BaseModel

from app.models.plan import BillingPeriod


class CreatePlan(BaseModel):
    hardware_id: int
    price: float
    billing_period: BillingPeriod
    plan_name: str
    plan_description: str
