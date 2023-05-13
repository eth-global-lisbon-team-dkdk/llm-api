from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from service.llm import LLM
from typing import List


app = FastAPI(
    title="LLM API",
    description="LLM API for the Ethglobal Hackathon",
    version="0.0.1",
)

llm = LLM()


@app.get("/")
async def root():
    return {"message": "Welcome to the LLM API"}


@app.get("/query")
async def query(query: str = Query(..., description="Query to ask the LLM")):
    return llm.main(query)
