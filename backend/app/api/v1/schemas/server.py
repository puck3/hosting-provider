from pydantic import BaseModel

from app.models.server import Status


class CreateServer(BaseModel):
    datacenter_id: int
    hardware_id: int
    status: Status
    operating_system: str


class CreateDatacenter(BaseModel):
    datacenter_name: str
    country: str
    city: str


class Country(BaseModel):
    country_name: str
