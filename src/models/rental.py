from pydantic import BaseModel
from datetime import datetime
from src.models.server import Server
from src.models.user import User
from src.models.plan import Plan


class Rental(BaseModel):
    rental_id: int
    server_id: int
    plan_id: int
    user: User
    start_at: datetime
    end_at: datetime
    update_at: datetime
