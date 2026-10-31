from dotenv import load_dotenv
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.store.redis.aio import AsyncRedisStore
import redis.asyncio as redis
from redisvl.index.index import SearchIndex
SearchIndex._reject_wrong_client_flavour = lambda self, client: None
import os
load_dotenv()

REDIS_URI = os.getenv('REDIS_URI') or 'redis://localhost:6379'

async def setup_redis_store():
    try:
        redis_client = redis.from_url(REDIS_URI)

        checkpointer = AsyncRedisSaver(redis_client=redis_client)
        store = AsyncRedisStore(redis_client=redis_client)

        await store.setup()
        await checkpointer.asetup()

        return store, checkpointer, redis_client
    except Exception as e:
        print('Something went wrong in setup_redis_store')
        raise e