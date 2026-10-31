from dotenv import load_dotenv
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.store.redis.aio import AsyncRedisStore
from redisvl.index.index import SearchIndex
SearchIndex._reject_wrong_client_flavour = lambda self, client: None
import os
load_dotenv()

REDIS_URI = os.getenv('REDIS_URI') or 'redis://localhost:6379'

async def setup_redis_store():

    try:
        async with (
            AsyncRedisStore.from_conn_string(REDIS_URI) as store,
            AsyncRedisSaver.from_conn_string(REDIS_URI) as checkpointer,
        ):
            await store.setup()
            await checkpointer.asetup()

            return store, checkpointer

    except Exception as e:
        print('Something went wrong in setup_redis_store')
        raise e