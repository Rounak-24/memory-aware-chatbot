from typing import TypedDict, Annotated
from langgraph.graph.message import BaseMessage, add_messages

class ChatState(TypedDict):
    user_id: str
    conv_id: str

    messages: Annotated[list[BaseMessage], add_messages]
    memory: str