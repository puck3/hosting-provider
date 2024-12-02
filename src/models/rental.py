from datetime import datetime, timedelta
from unittest import mock
from src.models.base import BaseModel
from src.models.plan import BillingPeriod
from src.models.server import Server
from src.models.user import User
from src.models.plan import Plan


class Rental(BaseModel):
    def __init__(
        self,
        rental_id: int,
        server: Server,
        plan: Plan,
        user: User,
        start_at: datetime,
        end_at: datetime,
        update_at: datetime,
    ) -> None:
        self._set_id(rental_id)
        self._server = server
        self._plan = plan
        self._user = user
        self._start_at = start_at
        self._end_at = end_at
        self._update_at = update_at

    def update_end_time(self) -> None:
        plan = self._plan.dict()
        match plan["billing_period"]:
            case BillingPeriod.hourly:
                self._end_at += timedelta(hours=1)

            case BillingPeriod.daily:
                self._end_at += timedelta(days=1)

            case BillingPeriod.monthly:
                self._end_at += timedelta(days=30)
