from datetime import datetime
from pydantic import BaseModel

from src.schemas.plan import BillingPeriod
from src.schemas.base import default_str, country_code_str
from src.schemas.server import ServerResponse
from src.schemas.user import UserResponse


class RentalRequest(BaseModel):
    config_id: int
    billing_period: BillingPeriod
    country: country_code_str
    city: default_str


class RentalResponse(BaseModel):
    rental_id: int
    server: ServerResponse
    user: UserResponse
    start_at: datetime
    end_at: datetime
