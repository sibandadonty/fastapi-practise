from redis.asyncio import Redis

REDIS_EXPIRY = 3600

token_blocklist = Redis(
    host="localhost",
    port=6379,
    db=0
)

async def add_token_to_blocklist(jti: str):
    await token_blocklist.set(name=jti, value="", ex=REDIS_EXPIRY)

async def token_in_blocklist(jti: str):
    result = await token_blocklist.get(jti)
    return result is not None