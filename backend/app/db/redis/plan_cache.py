import json
from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.db.redis.redis_client import get_redis_client


class PlanCache:
    def __init__(self, redis_client: Redis, cache_ttl: int = 300):
        self.r = redis_client
        self.cache_ttl = cache_ttl

    @staticmethod
    def get_cache_key(region: str) -> str:
        return f"plan_cache:{region}"

    async def cache_tariffs_region(self, region: str, plans: list[dict], ttl_sec: int = 300):
        key = self.get_cache_key(region)
        await self.r.setex(key, ttl_sec, json.dumps(plans))

    async def get_cached_tariffs_region(self, region: str) -> list[dict] | None:
        key = self.get_cache_key(region)
        data = await self.r.get(key)
        return json.loads(data) if data else None


def get_plan_cache(redis_client: Annotated[Redis, Depends(get_redis_client)]) -> PlanCache:
    return PlanCache(redis_client)
