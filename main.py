from fastapi import FastAPI
from schema import QueryRequest, QueryResponse
from graph import run_query

app = FastAPI(title="Enterprise Agentic RAG API")

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest) -> QueryResponse:
    answer = run_query(request.query)
    return QueryResponse(query=request.query, answer=answer)

@app.get("/health")
def health_check():
    return {"status": "ok"}