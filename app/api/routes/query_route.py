from fastapi import APIRouter, Depends
from app.api.controllers.query_controller import answer_controller
from app.api.dependencies import get_graph
from pydantic import BaseModel

query_router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    user_id: str
    conv_id: str


@query_router.post('/')
async def query_route(data:QuestionRequest, chatbot=Depends(get_graph)):
    return await answer_controller(data.question,data.user_id,data.conv_id,chatbot)