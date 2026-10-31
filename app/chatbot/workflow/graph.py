from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from app.chatbot.workflow.state import ChatState
from app.chatbot.workflow.nodes import (
    remember_node,
    chat_node,
    tool_node
)


graph_builder = StateGraph(ChatState)

graph_builder.add_node('remember_node',remember_node)
graph_builder.add_node('chat_node',chat_node)
graph_builder.add_node('tools',tool_node)

graph_builder.add_edge(START,'remember_node')
graph_builder.add_edge('remember_node','chat_node')

graph_builder.add_conditional_edges('chat_node', tools_condition)

graph_builder.add_edge('tools','chat_node')


async def compile_graph(store, checkpointer):
    try:
        return graph_builder.compile(store=store, checkpointer=checkpointer)
    
    except Exception as e:
        print('Something went wrong in compile_graph fn')
        raise e