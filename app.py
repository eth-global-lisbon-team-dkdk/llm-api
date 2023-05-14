from fastapi import FastAPI, Request
from pydantic import BaseModel
from service.llm import LLM
from service.mock_llm import MockLLM
from pathlib import Path
from fastapi import FastAPI, Request
from modal import Image, Stub, asgi_app, Mount
from fastapi.middleware.cors import CORSMiddleware

static_path = Path(__file__).with_name("service").resolve()


class QueryRequest(BaseModel):
    query: str


llm = LLM()


app = FastAPI(
    title="LLM API",
    description="LLM API for the Ethglobal Hackathon",
    version="0.0.1",
)
stub = Stub("llm-api-v2")
image = Image.debian_slim().pip_install("boto3", "langchain", "requests", "openai")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to the LLM API"}


@app.post("/query")
async def query(request: Request, query_request: QueryRequest):
    query = query_request.query
    return llm.main(query)


@stub.function(
    image=image,
    mounts=[Mount.from_local_dir(static_path, remote_path="/root/service")],
    container_idle_timeout=300,
    timeout=600,
)
@asgi_app()
def llm_app():
    return app
