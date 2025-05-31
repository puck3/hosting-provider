import json
from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.db.redis.redis_client import get_redis_client
from app.utils.logger import logger


class Publisher:
    def __init__(self, redis_client: Redis):
        self.r = redis_client

    async def publish_event(self, event_type: str, payload: dict):
        message = json.dumps(payload)
        await self.r.publish(event_type, message)
        logger.info(f"[publish] Отправлено событие: {event_type}")


async def get_publisher(redis_client: Annotated[Redis, Depends(get_redis_client)]) -> Publisher:
    return Publisher(redis_client)
