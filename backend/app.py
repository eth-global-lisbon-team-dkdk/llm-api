from fastapi import FastAPI


app = FastAPI(
    title="LLM API",
    description="LLM API for the Ethglobal Hackathon",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the LLM API"}


@app.get("/query")
async def query():
    return {"message": "Query the LLM API"}
