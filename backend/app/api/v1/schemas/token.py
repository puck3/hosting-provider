from pydantic import BaseModel

from app.core.config import ACCESS_TOKEN_CONFIG


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = ACCESS_TOKEN_CONFIG["expires_delta_minutes"] * 60
