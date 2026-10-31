from fastapi import Request
from langgraph.graph.state import CompiledStateGraph

def get_graph(request:Request)->CompiledStateGraph:
    if not hasattr(request.app.state, "chatbot"):
        raise RuntimeError("Graph is not initialized. Check app lifespan.")
    
    return request.app.state.chatbot