from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.core.config import REFRESH_TOKEN_CONFIG
from app.db.redis.redis_client import get_redis_client


class TokenRepository:
    def __init__(self, redis_client: Redis):
        self.r = redis_client
        self.ttl_min = REFRESH_TOKEN_CONFIG["expires_delta_minutes"]

    async def store_token(self, token: str, user_id: int):
        await self.r.setex(f"refresh_token:{token}", timedelta(minutes=self.ttl_min), user_id)

    async def get_user_id_by_token(self, token: str) -> int | None:
        val = await self.r.get(f"refresh_token:{token}")
        return int(val) if val else None


def get_token_repository(redis_client: Annotated[Redis, Depends(get_redis_client)]) -> TokenRepository:
    return TokenRepository(redis_client)
