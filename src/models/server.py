from enum import Enum

from src.models.hardware import Hardware
from src.models.base import BaseModel


class Status(str, Enum):
    active = "active"
    inactive = "inactive"


class Datacenter(BaseModel):
    def __init__(
        self, datacenter_id: int, datacenter_name: str, country: str, city: str
    ) -> None:
        self._set_id(datacenter_id)
        self._datacenter_name = datacenter_name
        self._country = country
        self._city = city


class Server(BaseModel):
    def __init__(
        self,
        server_id: int,
        datacenter: Datacenter,
        hardware: Hardware,
        status: Status,
        operating_system: str,
    ) -> None:
        self._set_id(server_id)
        self._datacenter = datacenter
        self._hardware = hardware
        self._status = status
        self._operating_system = operating_system

    def update_status(self, status: Status) -> None:
        self._status = status

    def is_available(self) -> bool:
        return self._status == Status.inactive

    def update_hardware(self, hardware: Hardware) -> None:
        self._hardware = hardware

    def update_os(self, operating_system: str):
        self._operating_system = operating_system
