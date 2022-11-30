import redis.asyncio
from fastapi_users.authentication import RedisStrategy

from core.settings import REDIS_PORT, REDIS_HOST

redis = redis.asyncio.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    print(redis)
    return RedisStrategy(redis, lifetime_seconds=3600)
