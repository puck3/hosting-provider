from typing import Annotated
from enum import Enum

from annotated_types import MaxLen
from pydantic import EmailStr

str_len = 50
long_str_len = 255
country_len = 2

default_str = Annotated[str, MaxLen(str_len)]
long_str = Annotated[str, MaxLen(long_str_len)]
email_str = Annotated[EmailStr, MaxLen(long_str_len)]
country_code_str = Annotated[str, MaxLen(country_len)]


class Role(str, Enum):
    user = "user"
    admin = "admin"


class Status(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    decommissioned = "decommissioned"


class BillingPeriod(str, Enum):
    hourly = "hourly"
    daily = "daily"
    monthly = "monthly"
