from fastapi import HTTPException
from app.chatbot.chat import chat


async def answer_controller(question:str, user_id:str, conv_id:str):
    try:
        if question==None or question=="" or user_id==None or conv_id==None:
            raise HTTPException(status_code=400, detail="question or user_id or conv_id is missing in the answer_controller....")

        answer = await chat(question,user_id, conv_id)  

        if answer==None or len(answer)==0:
            raise HTTPException(status_code=500, detail="answer is empty in the answer_controller....")

        return { 'answer':answer, 'success':True, 'status':200 }

    except Exception as e:
        if isinstance(e, HTTPException): raise e
        else: raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")