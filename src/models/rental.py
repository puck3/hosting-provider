from pydantic import BaseModel
from datetime import datetime, timedelta
from src.models.server import Server
from src.models.user import User
from src.models.plan import BillingPeriod, Plan


class Rental(BaseModel):
    rental_id: int
    user: User
    server: Server
    plan: Plan
    start_at: datetime
    end_at: datetime
    update_at: datetime

    def extend(self) -> None:
        match self.plan.billing_period:
            case BillingPeriod.hourly:
                self.end_at += timedelta(hours=1)

            case BillingPeriod.daily:
                self.end_at += timedelta(days=1)

            case BillingPeriod.monthly:
                self.end_at += timedelta(days=30)
