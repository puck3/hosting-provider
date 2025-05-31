from enum import Enum

from pydantic import BaseModel

from src.models.hardware import Hardware


class Status(str, Enum):
    available = "available"
    rented = "rented"


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
