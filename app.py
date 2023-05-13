from fastapi import FastAPI, Query
from service.llm import LLM


llm = LLM()


app = FastAPI(
    title="LLM API",
    description="LLM API for the Ethglobal Hackathon",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the LLM API"}


@app.get("/query")
async def query(
    query: str = Query(..., title="Query", description="Query to send to LLM")
):
    return llm.main(query)
