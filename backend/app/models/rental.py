from datetime import datetime, timedelta

from pydantic import BaseModel

from app.models.plan import BillingPeriod
from app.models.server import Server


class UserData(BaseModel):
    user_id: int
    login: str
    email: str


class Rental(BaseModel):
    rental_id: int
    user: UserData
    server: Server
    price: float
    billing_period: BillingPeriod
    start_at: datetime
    end_at: datetime
    update_at: datetime

    def extend(self) -> None:
        match self.billing_period:
            case BillingPeriod.hourly:
                self.end_at += timedelta(hours=1)

            case BillingPeriod.daily:
                self.end_at += timedelta(days=1)

            case BillingPeriod.monthly:
                self.end_at += timedelta(days=30)
