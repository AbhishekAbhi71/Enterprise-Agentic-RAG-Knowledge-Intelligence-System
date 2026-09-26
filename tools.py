from langchain_core.tools import tool
from rag import hybrid_retriever, rerank_documents, rewrite_chain
from sql_db import run_sql_query

@tool
def rag_route(query: str) -> str:
    """
    Rewrite the user's query, perform hybrid retrieval,
    rerank the retrieved documents, and return the
    highest-quality evidence.
    """
    rewritten_response = rewrite_chain.invoke({"query": query})
    rewritten_query = rewritten_response.content

    retrieved_docs = hybrid_retriever.invoke(rewritten_query)
    reranked_docs = rerank_documents(rewritten_query, retrieved_docs, top_n=5)

    evidence = "\n\n".join(
        f"""
Source: {doc.metadata.get('document_name', 'Unknown')}
Page: {doc.metadata.get('page_number', 'N/A')}
Section: {doc.metadata.get('section', 'Unknown')}

Content:
{doc.page_content}
"""
        for doc in reranked_docs
    )
    return evidence

@tool
def sql_route(query: str) -> str:
    """
    Use this tool when the answer requires structured data
    from PostgreSQL.
    """
    result = run_sql_query(query)
    return str(result)

@tool
def hybrid_route(query: str) -> str:
    """
    Use this tool when BOTH company documents and PostgreSQL
    database information are required.
    """
    rewritten_response = rewrite_chain.invoke({"query": query})
    rewritten_query = rewritten_response.content

    retrieved_docs = hybrid_retriever.invoke(rewritten_query)
    reranked_docs = rerank_documents(rewritten_query, retrieved_docs, top_n=5)

    evidence = "\n\n".join(
        f"""
Source: {doc.metadata.get('document_name', 'Unknown')}
Page: {doc.metadata.get('page_number', 'N/A')}
Section: {doc.metadata.get('section', 'Unknown')}

Content:
{doc.page_content}
"""
        for doc in reranked_docs
    )

    sql_result = run_sql_query(query)

    return str(
        {
            "documents": evidence,
            "sql_query": sql_result["sql_query"],
            "database_rows": sql_result["database_rows"],
        }
    )

tools = [rag_route, sql_route, hybrid_route]