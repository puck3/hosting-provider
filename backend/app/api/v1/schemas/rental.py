from pydantic import BaseModel


class CreateRental(BaseModel):
    plan_id: int
    country: str
