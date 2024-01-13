from redis import asyncio as aioredis


async def get_redis() -> aioredis.Redis:
    redis = await aioredis.from_url(
        url='url_to_my_redis_db',
        decode_responses=True)
    try:
        yield redis
    finally:
        redis.close()
        await redis.close()