from app.llm.openai_llm import openai
from app.memory.memory_models import MemoryDecision
from langgraph.store.base import BaseStore
from langchain_core.messages import SystemMessage

memory_extractor_llm = openai.with_structured_output(MemoryDecision)

MEMORY_PROMPT = """You are responsible for updating and maintaining accurate user memory.

CURRENT USER DETAILS (existing memories):
{user_details_content}

TASK:
- Review the user's latest message.
- Extract user-specific info worth storing long-term (identity, stable preferences, ongoing projects/goals).
- For each extracted item, set is_new=true ONLY if it adds NEW information compared to CURRENT USER DETAILS.
- If it is basically the same meaning as something already present, set is_new=false.
- Keep each memory as a short atomic sentence.
- No speculation; only facts stated by the user.
- If there is nothing memory-worthy, return should_write=false and an empty list.
"""


async def extract_memory(query:str, store:BaseStore, user_id:str, existing:str)->MemoryDecision:
    try:
        decision:MemoryDecision = await memory_extractor_llm.ainvoke([
            SystemMessage(content=MEMORY_PROMPT.format(user_details_content=existing)),
            {'role':'user', 'content': query}
        ])

        return decision
    
    except Exception as e:
        print('Something went wrong in extract_memory')
        raise e