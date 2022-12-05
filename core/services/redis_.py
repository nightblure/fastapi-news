from aioredis import Redis
import aioredis
from fastapi import Depends
from fastapi_users.authentication import RedisStrategy

from core.settings import REDIS_PORT, REDIS_HOST

redis_url = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# print(redis_url)

# redis = aioredis.Redis.from_url(redis_url, decode_responses=True)


async def get_redis_client():
    async with aioredis.Redis.from_url(redis_url, decode_responses=True) as redis_client:
        yield redis_client


def get_redis_strategy(redis_client: Redis = Depends(get_redis_client)) -> RedisStrategy:
    return RedisStrategy(redis_client, lifetime_seconds=300)
