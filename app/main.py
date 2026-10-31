from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes.query_route import query_router
from app.services.redis import setup_redis_store
from app.chatbot.workflow.graph import compile_graph


@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        store, checkpointer, redis_client = await setup_redis_store()
        app.state.chatbot = await compile_graph(store, checkpointer)
        yield

        redis_client.close()

    except Exception as e:
        print('Error while initialising lifespan....',e)  

app = FastAPI(lifespan=lifespan)

app.include_router(router=query_router,prefix="/query")

@app.get("/health")
async def health_handler():
    return {
        "status":"ok",
        "success":True,
        "message":"Server is up & running...."
    }

def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )

if __name__=="__main__":
    main()