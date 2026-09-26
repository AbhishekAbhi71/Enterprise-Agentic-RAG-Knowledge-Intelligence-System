from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., description="User question to the RAG system")

class QueryResponse(BaseModel):
    query: str
    answer: str
    evidence: str | None = None