from enum import Enum
from pydantic import BaseModel

from src.core.constants import default_str, country_code_str
from src.schemas.hardware_config import HardwareConfigResponse


class Status(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    decommissioned = "decommissioned"


class Datacenter(BaseModel):
    datacenter_id: int | None
    name: default_str
    country: country_code_str
    city: default_str


class ServerBase(BaseModel):
    status: Status
    operating_system: default_str


class ServerResponse(ServerBase):
    server_id: int
    datacenter: Datacenter
    config: HardwareConfigResponse


class ServerRequest(ServerBase):
    datacenter_id: int
    config_id: int
