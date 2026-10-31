from app.chatbot.workflow.state import ChatState
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph


async def chat(question:str, user_id:str, conv_id:str, chatbot:CompiledStateGraph):
    try:
        if user_id==None or conv_id==None:
            raise Exception('user_id or conv_id is missing')

        config = {"configurable": {"thread_id": conv_id}} 
        messages = [HumanMessage(content=question)]

        initial_state = ChatState(
            user_id=user_id,
            conv_id=conv_id,
            messages=messages
        )

        final_state:ChatState = await chatbot.ainvoke(initial_state, config)
        return final_state['messages'][-1].content

    except Exception as e:
        print('Something went wrong in chat fn',e)
        raise e