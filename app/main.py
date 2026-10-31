from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from app.api.routes.query_route import query_router

app = FastAPI()

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