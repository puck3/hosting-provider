from pydantic import BaseModel


class CreateRental(BaseModel):
    user_id: int
    plan_id: int
    country: str
