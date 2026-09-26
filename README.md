# Enterprise Agentic RAG Knowledge Intelligence System

An enterprise-style Agentic RAG system that combines **LLM reasoning, LangGraph-based tool routing, hybrid document retrieval, reranking, PostgreSQL SQL querying, answer generation, and verification**.

The system can intelligently determine whether a user query requires information from unstructured documents, structured database data, or both.

## 🚀 Key Features

* 🤖 Agentic workflow using LangGraph
* 🧠 Gemini LLM integration
* 🔀 Intelligent query routing
* 📄 PDF document ingestion
* 🔎 Hybrid retrieval using:

  * Dense vector search
  * BM25 sparse retrieval
* 🎯 Cross-encoder reranking
* ✍️ LLM-based query rewriting
* 🗄️ PostgreSQL database integration
* 🔧 SQL generation and execution through an agent tool
* 🔗 Hybrid document + SQL queries
* 🛡️ Read-only SQL protection
* ✅ Answer verification
* 📚 Source/page-aware document evidence
* ⚡ Qdrant vector database
* 🚀 FastAPI backend
* ⚛️ React frontend planned

---

## 🏗️ Architecture

```text
                         User Query
                              │
                              ▼
                       ┌──────────────┐
                       │   FastAPI    │
                       │    Backend   │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  LangGraph   │
                       │ Agent Router │
                       └──────┬───────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
          ┌──────────┐  ┌──────────┐  ┌───────────┐
          │ RAG Tool │  │ SQL Tool │  │Hybrid Tool│
          └────┬─────┘  └────┬─────┘  └─────┬─────┘
               │             │              │
               ▼             ▼              ▼
        Query Rewrite   SQL Generation   Query Rewrite
               │             │              │
               ▼             ▼              ▼
        Hybrid Search   PostgreSQL      Hybrid Search
        ┌──────┴──────┐                  │
        │             │                  ▼
        ▼             ▼             Reranking
     Qdrant         BM25                │
        │             │                  │
        └──────┬──────┘                  │
               ▼                         │
           Reranking ◄───────────────────┘
               │
               ▼
        Evidence / SQL Results
               │
               ▼
       ┌─────────────────┐
       │ Answer Generator│
       └────────┬────────┘
                │
                ▼
          ┌───────────┐
          │ Verifier  │
          └─────┬─────┘
                │
                ▼
         Final Answer
```

---

## 🧠 Query Routing

The system uses an LLM-powered router to select exactly one tool.

### 1. RAG Route

Used when the answer requires information from company documents or policies.

Example:

```text
What is the maximum hotel reimbursement per night?
```

Flow:

```text
User Query
   ↓
Query Rewriting
   ↓
Hybrid Retrieval
   ↓
Reranking
   ↓
Evidence
```

### 2. SQL Route

Used when the answer requires structured PostgreSQL data.

Example:

```text
How many employees are in Finance?
```

Flow:

```text
User Query
   ↓
SQL Generation
   ↓
Read-only SQL Validation
   ↓
PostgreSQL
   ↓
Database Results
```

### 3. Hybrid Route

Used when both company policies and database information are required.

Example:

```text
According to the leave policy, how many employees
are eligible for 30 days of annual leave?
```

Flow:

```text
User Query
       │
       ├───────────────┐
       ▼               ▼
 Document Retrieval   PostgreSQL
       │               │
       ▼               ▼
   Reranking        SQL Results
       │               │
       └───────┬───────┘
               ▼
         Answer Generator
               │
               ▼
            Verifier
```

---

## 🔍 Advanced RAG Pipeline

The document retrieval pipeline uses:

```text
User Query
    ↓
Query Rewriting
    ↓
Dense Retrieval ───────┐
                       ├── Hybrid Retrieval
BM25 Retrieval ────────┘
    ↓
Cross-Encoder Reranking
    ↓
Top Evidence
```

### Dense Retrieval

Uses Gemini embeddings with Qdrant.

### Sparse Retrieval

Uses BM25 to retrieve documents based on keyword relevance.

### Hybrid Retrieval

Combines dense and sparse retrieval:

```python
EnsembleRetriever(
    retrievers=[dense_retriever, sparse_retriever],
    weights=[0.5, 0.5]
)
```

### Reranking

Retrieved documents are reranked using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

## 🗄️ Database Layer

The system uses PostgreSQL for structured enterprise data.

Example employee fields:

```text
id
name
department
years_of_service
salary
join_date
```

The SQL tool generates SQL from natural-language questions and executes only read-oriented queries.

The system rejects generated queries that do not begin with:

```text
SELECT
```

or

```text
WITH
```

This provides a basic read-only protection layer for the SQL tool.

---

## 🛡️ Answer Verification

After generating an answer, a separate verification step checks the response against the retrieved evidence.

```text
Evidence
   ↓
Answer Generator
   ↓
Draft Answer
   ↓
Verifier
   ↓
Final Answer
```

The verifier is instructed to:

* Preserve supported claims
* Remove unsupported claims
* Avoid outside knowledge
* Answer directly
* Report insufficient evidence when necessary

---

## 🛠️ Tech Stack

| Category               | Technology                          |
| ---------------------- | ----------------------------------- |
| Language               | Python                              |
| LLM                    | Google Gemini                       |
| Agent Framework        | LangGraph                           |
| LLM Framework          | LangChain                           |
| Vector Database        | Qdrant                              |
| Sparse Retrieval       | BM25                                |
| Embeddings             | Gemini Embeddings                   |
| Reranker               | Sentence Transformers Cross-Encoder |
| Relational Database    | PostgreSQL                          |
| API Backend            | FastAPI                             |
| Frontend               | React *(planned)*                   |
| Environment Management | python-dotenv                       |
| Containerization       | Docker *(where applicable)*         |

---

## 📁 Project Structure

```text
enterprise-agentic-rag/
│
├── app/
│   ├── main.py
│   ├── agents/
│   │   └── graph.py
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── embeddings.py
│   ├── database/
│   │   ├── postgres.py
│   │   └── sql_tools.py
│   └── tools/
│       └── retrieval_tools.py
│
├── data/
│   └── ...
│
├── frontend/
│   └── ...
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-agentic-rag
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv myenv
```

Activate it:

```powershell
.\myenv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GOOGLE_API_KEY=your_api_key

POSTGRES_URL=your_postgresql_connection_string

QDRANT_URL=http://localhost:6333

PDF_PATH=./data/employee_policy_handbook_complete.pdf
```

Do not commit `.env` to GitHub.

---

## 🐳 Run Qdrant

Make sure Qdrant is running locally.

Default configuration:

```text
http://localhost:6333
```

The application creates/populates the required vector collection.

---

## 🗄️ Configure PostgreSQL

Create your PostgreSQL database and required tables.

Then configure:

```env
POSTGRES_URL=your_postgresql_connection_string
```

---

## ▶️ Run the Backend

Start FastAPI with:

```powershell
uvicorn app.main:app --reload
```

The API will be available locally.

Once the React frontend is added, it can communicate with the FastAPI backend through the API endpoints.

---

## 🧪 Example Queries

### Document Query

```text
What is the maximum hotel reimbursement per night?
```

### Database Query

```text
How many employees are in Finance?
```

### Hybrid Query

```text
According to the leave policy, how many employees
are eligible for 30 days of annual leave?
```

### Unknown Document Query

```text
What is the company's travel insurance provider?
```

### Database Query

```text
How many employees joined in 2019?
```

---

## 🔐 Security Notes

Sensitive configuration should never be committed to the repository.

The following files should remain local:

```text
.env
```

API keys, database passwords, private connection strings, and other secrets must be stored in environment variables.

---

## 🚧 Future Improvements

* React-based ChatGPT-style frontend
* Redis caching
* Background ingestion jobs
* RAG evaluation pipeline
* Retrieval and answer-quality metrics
* Authentication and authorization
* Document-level access control
* Streaming responses
* Conversation memory
* Docker Compose deployment
* Production deployment

---

## 🎯 Project Goal

The goal of this project is to demonstrate how an enterprise knowledge system can combine:

```text
LLM
+
Agentic Workflows
+
Advanced RAG
+
Vector Search
+
Keyword Search
+
Reranking
+
SQL
+
Verification
+
API Backend
```

into a single intelligent knowledge system capable of answering questions across both unstructured enterprise documents and structured business data.
