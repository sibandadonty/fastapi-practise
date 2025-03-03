import redis.asyncio as aioredis
from src.config import settings

token_blocklist = aioredis.from_url(settings.REDIS_URL)

JTI_EXPIRY = 3600

async def add_jti_to_blocklist(jti: str):
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str):
    jti = await token_blocklist.get(jti)
    return jti is not None