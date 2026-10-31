from langgraph.store.base import BaseStore, PutOp
from app.memory.memory_models import MemoryDecision
import uuid


async def retrieve_memory(query:str, store:BaseStore, user_id:str):
    try:
        namespace = ('users', 'memories', user_id,)
        memories = await store.asearch(namespace, query=query, limit=5)
        
        return "\n".join(memory.value['data'] for memory in memories) if memories else "(empty)"

    except Exception as e:
        print('Something went wrong in retrieve_memory')
        raise e


async def save_memory(decision:MemoryDecision, user_id:str, store:BaseStore):
    try:
        namespace = ('users', 'memories', user_id,)
        operations:list[PutOp] = []

        if decision.should_write:
            for mem in decision.memories:
                if mem.is_new: 
                    op = PutOp(
                        namespace=namespace,
                        key=str(uuid.uuid4()),
                        value={ 'data':mem.text }
                    )

                    operations.append(op)
                    
        if operations and len(operations)>0: await store.abatch(operations)
        
    except Exception as e:
        print('Something went wrong in save_memory')
        raise e