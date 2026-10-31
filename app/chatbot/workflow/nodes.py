from langsmith import traceable
from app.chatbot.workflow.state import ChatState
from app.memory.memory_store import save_memory, retrieve_memory
from langgraph.store.base import BaseStore
from app.memory.memory_extractor import extract_memory
from app.chatbot.chat_llm import SYSTEM_PROMPT_TEMPLATE, chat_llm
from langchain_core.messages import SystemMessage, RemoveMessage
from langgraph.prebuilt import ToolNode
from app.chatbot.tools.web_search import tools
from dotenv import load_dotenv
load_dotenv()


@traceable(name='remember_node')
async def remember_node(state:ChatState, store:BaseStore):
    query = state['messages'][-1].content
    user_id = state['user_id']

    existing = await retrieve_memory(query,store,user_id)
    decision = await extract_memory(query,store,user_id,existing)
    await save_memory(decision,user_id,store)

    return { 'memory':existing }


@traceable(name='chat_node')
async def chat_node(state:ChatState):
    messages = state['messages']
    memories = state['memory']

    answer = await chat_llm.ainvoke([
        SystemMessage(SYSTEM_PROMPT_TEMPLATE.format(user_details_content=memories)),
        *messages
    ])

    messages.append(answer)
    if(len(messages)>5): 
        messages_to_delete = messages[:-5]
        delete_commands = [RemoveMessage(id=m.id) for m in messages_to_delete]
        return { 'messages': [answer] + delete_commands }

    return { 'messages': [answer] }

tool_node = ToolNode(tools)