from fastapi import APIRouter
from app.api.controllers.query_controller import answer_controller
from pydantic import BaseModel

query_router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    user_id: str
    conv_id: str


@query_router.post('/')
async def query_route(data:QuestionRequest):
    answer = await answer_controller(data.question,data.user_id,data.conv_id)
    
    return {
        'answer':answer,
        'success':True,
        'status':200
    }