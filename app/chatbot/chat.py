from app.chatbot.workflow.graph import chatbot
from app.chatbot.workflow.state import ChatState
from langchain_core.messages import HumanMessage


async def chat(question:str, user_id:str, conv_id:str):
    try:
        if user_id==None or conv_id==None:
            raise Exception('user_id or conv_id is missing')

        config = {"configurable": {"thread_id": conv_id}} 
        messages = [HumanMessage(content=question)]

        initial_state = ChatState(
            user_id, conv_id, messages
        )

        final_state = await chatbot.ainvoke(initial_state, config)
        print(final_state)
        return final_state

    except Exception as e:
        print('Something went wrong in chat fn')
        raise e