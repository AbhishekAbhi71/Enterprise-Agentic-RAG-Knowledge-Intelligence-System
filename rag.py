from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_classic.retrievers import EnsembleRetriever, BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from qdrant_client import QdrantClient
from sentence_transformers import CrossEncoder

from config import (
    CLEANED_GEMINI_KEY,
    PDF_PATH,
    QDRANT_URL,
    QDRANT_COLLECTION,
)

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=CLEANED_GEMINI_KEY,
)

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(docs)

for i, chunk in enumerate(chunks):
    chunk.metadata.update({
        "id": f"doc_{i}",
        "document_name": PDF_PATH.split("\\")[-1],
        "chunk_index": i,
        "section": chunk.metadata.get("section", "unknown"),
        "page_number": chunk.metadata.get("page_number", "N/A"),
    })

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=CLEANED_GEMINI_KEY,
)

client = QdrantClient(url=QDRANT_URL)
client.delete_collection(QDRANT_COLLECTION)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name=QDRANT_COLLECTION,
)

dense_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
sparse_retriever = BM25Retriever.from_documents(chunks)

hybrid_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, sparse_retriever],
    weights=[0.5, 0.5],
)

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query: str, documents, top_n: int = 5):
    pairs = [(query, doc.page_content) for doc in documents]
    scores = cross_encoder.predict(pairs)
    ranked_docs = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked_docs[:top_n]]

rewrite_prompt = PromptTemplate(
    input_variables=["query"],
    template="""Rewrite the query to be more precise and retrieval-friendly.

Original: {query}

Rewritten:""",
)

rewrite_chain = rewrite_prompt | llm