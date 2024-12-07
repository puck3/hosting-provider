from pydantic import BaseModel
from enum import Enum

from src.models.hardware import Hardware


class Status(str, Enum):
    available = "Доступен"
    rented = "В аренде"


class Datacenter(BaseModel):
    datacenter_id: int
    datacenter_name: str
    country: str
    city: str


class Server(BaseModel):
    server_id: int
    datacenter: Datacenter
    hardware: Hardware
    status: Status
    operating_system: str
