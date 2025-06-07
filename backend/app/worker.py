import asyncio
import json

from app.db.redis.redis_client import get_redis_client
from app.utils.logger import logger


async def server_setup_worker():
    redis = await get_redis_client()
    pubsub = redis.pubsub()
    await pubsub.subscribe("server_created")

    logger.info("Server setup worker started")
    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
            if message:
                data = json.loads(message["data"])
                logger.info(
                    f"Server {data['server_id']} created at datacenter {data['datacenter_id']}. Starting server setup..."
                )

                await asyncio.sleep(5)

                logger.info(f"Server {data['server_id']} configured!")
        except Exception as e:
            logger.error(f"Error in server_setup_worker: {e}")
            await asyncio.sleep(5)


async def rental_activation_worker():
    redis = await get_redis_client()
    pubsub = redis.pubsub()
    await pubsub.subscribe("rental_created")

    logger.info("Rental activation worker started")
    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
            if message:
                data = json.loads(message["data"])
                logger.info(f"Rental {data['rental_id']} created for user {data['user_id']}")
                logger.info(f"Rented server: {data['server_id']}")

                await asyncio.sleep(3)

                logger.info(f"Rental {data['rental_id']} activated!")
        except Exception as e:
            logger.error(f"Error in rental_activation_worker: {e}")
            await asyncio.sleep(5)
