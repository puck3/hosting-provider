from datetime import datetime
from pydantic import BaseModel

from src.core.constants import long_str
from src.schemas.user import UserResponse


class BackupBase(BaseModel):
    filename: long_str
    description: str


class BackupResponse(BackupBase):
    backup_id: int
    created_at: datetime
    created_by: UserResponse


BackupRequest = BackupBase
