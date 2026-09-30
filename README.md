# 🚀 Enterprise Agentic RAG Knowledge Intelligence System

> **A full-stack AI-powered enterprise knowledge intelligence platform built withHTML/CSS/JavaScript and FastAPI, combining Agentic RAG, LangGraph, LangChain, Gemini, Qdrant, PostgreSQL, hybrid search, cross-encoder reranking, SQL reasoning, and answer verification.**

This project is designed as an **enterprise-style full-stack AI application** capable of answering questions from both **unstructured company documents** and **structured business databases**.

The system intelligently determines whether a query requires:

* 📄 Document-based retrieval
* 🗄️ PostgreSQL database information
* 🔗 Both document and database information

---

# 🌟 Full-Stack Architecture

This project follows a modern **Frontend → API → Agent → Data Layer** architecture.

```text
                         ┌─────────────────────────┐
                         │      HTML/CSS/JavaScript
                                     Frontend     │
                         │                         │
                         │  Chat Interface / UI    │
                         └────────────┬────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌─────────────────────────┐
                         │     FastAPI Backend      │
                         │                         │
                         │  API Routes / Services  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      LangGraph Agent     │
                         │                         │
                         │     Query Analyzer      │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌────────────┐    ┌────────────┐    ┌────────────┐
             │  RAG Tool  │    │  SQL Tool  │    │Hybrid Tool │
             └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
                   │                 │                  │
                   ▼                 ▼                  ▼
             Query Rewrite      SQL Generation      Query Rewrite
                   │                 │                  │
                   ▼                 ▼                  ▼
             Hybrid Search      PostgreSQL        Hybrid Search
              ┌────┴────┐                            │
              │         │                            ▼
              ▼         ▼                       Reranking
           Qdrant     BM25                          │
              │         │                            │
              └────┬────┘                            │
                   ▼                                 │
              Reranking ◄────────────────────────────┘
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
              │  Verifier │
              └─────┬─────┘
                    │
                    ▼
             Final Answer
                    │
                    ▼
              React Frontend
```

---

# 🧩 Full-Stack Components

## 🎨 Frontend — HTML/CSS/JavaScript

The frontend is built using *HTML/CSS/JavaScripts** and provides the user-facing interface for interacting with the AI knowledge system.

The React frontend communicates with the backend through REST APIs exposed by FastAPI.

### Frontend responsibilities

* 💬 Chat/query interface
* 📤 Send user questions to the backend
* 📥 Display AI-generated answers
* 📚 Display retrieved evidence and sources
* ⚡ Handle API responses
* 🔄 Loading and error states
* 📊 Present structured database results

```text
HTML/CSS/JavaScript
    │
    │ HTTP / REST API
    ▼
FastAPI
```

---

# ⚡ Backend — FastAPI

The backend is built using **FastAPI** and acts as the API layer between the React frontend and the Agentic RAG system.

### Backend responsibilities

* API endpoints
* Request validation
* Agent execution
* LangGraph workflow execution
* RAG pipeline execution
* PostgreSQL interaction
* Qdrant interaction
* Response generation
* Error handling

```text
React
  ↓
FastAPI
  ↓
LangGraph
  ↓
Agentic RAG
```

---

# 🤖 Agentic AI Architecture

The core intelligence of the application is implemented using **LangGraph**.

The system does not use a fixed retrieval path for every question.

Instead, an LLM-powered routing agent determines which tool should handle the query.

### Available tools

```text
                    User Query
                        │
                        ▼
                Query Analyzer
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       RAG Tool      SQL Tool     Hybrid Tool
```

---

# 🔀 Intelligent Query Routing

## 1️⃣ RAG Route

Used when the answer exists inside company documents or policies.

### Example

```text
What is the maximum hotel reimbursement per night?
```

Pipeline:

```text
User Query
    ↓
Query Rewriting
    ↓
Hybrid Retrieval
    ↓
Cross-Encoder Reranking
    ↓
Relevant Evidence
    ↓
LLM Answer
```

---

# 2️⃣ SQL Route

Used when structured information is required from PostgreSQL.

### Example

```text
How many employees are in Finance?
```

Pipeline:

```text
User Query
    ↓
SQL Generation
    ↓
SQL Validation
    ↓
PostgreSQL
    ↓
Database Results
    ↓
LLM Answer
```

The system allows only read-oriented SQL queries beginning with:

```text
SELECT
```

or:

```text
WITH
```

---

# 3️⃣ Hybrid Route

Used when both documents and structured database information are required.

### Example

```text
According to the leave policy,
how many employees are eligible for 30 days of annual leave?
```

Pipeline:

```text
                    User Query
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Document Retrieval       PostgreSQL
              │                     │
              ▼                     ▼
          Reranking             SQL Results
              │                     │
              └──────────┬──────────┘
                         ▼
                  Answer Generator
                         │
                         ▼
                     Verifier
                         │
                         ▼
                   Final Answer
```

---

# 🔍 Advanced RAG Pipeline

The document retrieval system uses an advanced multi-stage RAG pipeline.

```text
User Query
     ↓
Query Rewriting
     ↓
┌───────────────────────┐
│   Hybrid Retrieval    │
│                       │
│ Dense + Sparse Search │
└───────────┬───────────┘
            ↓
      Candidate Documents
            ↓
    Cross-Encoder Reranker
            ↓
       Top Documents
            ↓
         Evidence
            ↓
      Answer Generator
```

---

# 🔎 Hybrid Search

The project combines two retrieval strategies.

### Dense Retrieval

Uses:

* Gemini Embeddings
* Qdrant Vector Database

```text
Query
  ↓
Gemini Embedding
  ↓
Qdrant
  ↓
Semantic Matches
```

### Sparse Retrieval

Uses:

* BM25

This helps retrieve documents based on exact keyword matches.

### Combined Retrieval

```python
EnsembleRetriever(
    retrievers=[
        dense_retriever,
        sparse_retriever
    ],
    weights=[0.5, 0.5]
)
```

This combines semantic and keyword-based retrieval.

---

# 🎯 Cross-Encoder Reranking

After hybrid retrieval, the retrieved documents are reranked using a Cross-Encoder.

Model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Pipeline:

```text
Hybrid Retrieval
       ↓
Candidate Documents
       ↓
Cross Encoder
       ↓
Relevance Scores
       ↓
Top-K Documents
```

This reduces the possibility of passing irrelevant retrieved documents to the LLM.

---

# ✍️ Query Rewriting

Before retrieval, the original user query is rewritten into a more retrieval-friendly form.

```text
Original Query
      ↓
LLM Query Rewriter
      ↓
Optimized Query
      ↓
Retriever
```

This improves retrieval for ambiguous or poorly formulated questions.

---

# 🗄️ PostgreSQL Integration

PostgreSQL is used for structured enterprise information.

Example employee table:

```text
employees
├── id
├── name
├── department
├── years_of_service
├── salary
└── join_date
```

Example query:

```text
How many employees are in Finance?
```

The system:

```text
Natural Language Question
          ↓
      SQL Generator
          ↓
      SQL Validation
          ↓
       PostgreSQL
          ↓
      Query Results
```

---

# 🛡️ SQL Safety

The generated SQL is validated before execution.

Only read-only queries beginning with:

```text
SELECT
```

or:

```text
WITH
```

are allowed.

Queries attempting to perform operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
```

are rejected by the application layer.

---

# 🧠 Answer Generation

After the selected tool returns evidence, the answer generator produces the final response.

The model is instructed to:

* Use only retrieved evidence
* Avoid hallucinating information
* Answer the user's question directly
* Mention relevant sources
* Use PostgreSQL results when applicable
* Combine document and database evidence for hybrid queries

---

# ✅ Answer Verification

A separate verification stage checks the generated answer against the available evidence.

```text
Retrieved Evidence
       ↓
Answer Generator
       ↓
Draft Answer
       ↓
Verifier
       ↓
Final Answer
```

The verifier:

* Preserves supported claims
* Removes unsupported claims
* Does not introduce outside knowledge
* Checks the answer against the evidence
* Reports insufficient evidence when appropriate

---

# 🏗️ Project Structure

```text
Enterprise-Agentic-RAG-Knowledge-Intelligence-System/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── agents/
│   │   │   └── graph.py
│   │   │
│   │   ├── rag/
│   │   │   ├── retriever.py
│   │   │   ├── reranker.py
│   │   │   └── embeddings.py
│   │   │
│   │   ├── database/
│   │   │   ├── postgres.py
│   │   │   └── sql_tools.py
│   │   │
│   │   └── tools/
│   │       └── retrieval_tools.py
│   │
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── data/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

> The exact folder structure may evolve as additional frontend, backend, evaluation, and deployment components are added.

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| React.js   | Frontend UI                      |
| JavaScript | Frontend logic                   |
| HTML/CSS   | UI structure and styling         |
| REST API   | Frontend ↔ Backend communication |

## Backend

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Core backend language        |
| FastAPI       | REST API backend             |
| LangGraph     | Agent workflow orchestration |
| LangChain     | LLM and RAG framework        |
| Google Gemini | LLM and embeddings           |

## AI / RAG

| Technology        | Purpose                |
| ----------------- | ---------------------- |
| Qdrant            | Vector database        |
| Gemini Embeddings | Dense embeddings       |
| BM25              | Sparse retrieval       |
| EnsembleRetriever | Hybrid retrieval       |
| Cross-Encoder     | Document reranking     |
| Query Rewriting   | Retrieval optimization |

## Database

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| PostgreSQL          | Structured enterprise data |
| SQLAlchemy          | Database connectivity      |
| LangChain SQL tools | Natural language → SQL     |

## Infrastructure

| Technology | Purpose                |
| ---------- | ---------------------- |
| Docker     | Containerized services |
| Qdrant     | Vector search service  |
| PostgreSQL | Relational database    |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/AbhishekAbhi71/Enterprise-Agentic-RAG-Knowledge-Intelligence-System.git

cd Enterprise-Agentic-RAG-Knowledge-Intelligence-System
```

---

# 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv myenv
```

Activate it:

```powershell
.\myenv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 3. Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key

POSTGRES_URL=postgresql://username:password@localhost:5432/database_name

QDRANT_URL=http://localhost:6333

PDF_PATH=./data/employee_policy_handbook_complete.pdf
```

### ⚠️ Important

Never commit your actual `.env` file.

The repository only contains:

```text
.env.example
```

API keys, passwords, and private connection strings should remain in your local environment.

---

# 4. Start Qdrant

Make sure Qdrant is running locally.

Default URL:

```text
http://localhost:6333
```

Example Docker command:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

# 5. Configure PostgreSQL

Create your PostgreSQL database and required tables.

Then configure the connection string:

```env
POSTGRES_URL=your_postgresql_connection_string
```

---

# 6. Start FastAPI Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The FastAPI backend will start locally.

---

# 7. Start React Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The React frontend will communicate with the FastAPI backend through REST APIs.

---

# 🔄 Complete Request Flow

A typical request travels through the entire full-stack system:

```text
┌───────────────────────┐
│      React UI         │
│                       │
│ User enters question │
└───────────┬───────────┘
            │
            │ HTTP Request
            ▼
┌───────────────────────┐
│    FastAPI Backend    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│     LangGraph Agent   │
│                       │
│    Query Analyzer     │
└───────────┬───────────┘
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
    RAG    SQL   HYBRID
     │      │      │
     ▼      ▼      ▼
  Qdrant PostgreSQL Both
     │      │      │
     └──────┼──────┘
            ▼
       Reranking
            ↓
     Answer Generator
            ↓
         Verifier
            ↓
       Final Answer
            ↓
       FastAPI Response
            ↓
        React UI
```

---

# 🧪 Example Queries

### 📄 Document Query

```text
What is the maximum hotel reimbursement per night?
```

### 🗄️ Database Query

```text
How many employees are in Finance?
```

### 🔗 Hybrid Query

```text
According to the leave policy,
how many employees are eligible for 30 days of annual leave?
```

### 📄 Another Document Query

```text
Who owns the Remote Work Policy?
```

### 🗄️ Database Query

```text
How many employees joined in 2019?
```

---

# 🔐 Security Considerations

Sensitive information should never be committed to GitHub.

The following should remain private:

```text
.env
API Keys
Database Passwords
Private Connection Strings
Private Documents
```

The `.gitignore` file prevents sensitive local files from being committed.

---

# 🚧 Future Enhancements

* ⚛️ Enhanced React ChatGPT-style interface
* 🔐 Authentication and authorization
* 👥 Role-based document access
* 📚 Multi-document ingestion
* 📊 RAG evaluation framework
* 📈 Retrieval evaluation metrics
* 🧪 Automated evaluation dataset
* ⚡ Redis caching
* 🔄 Background document processing
* 💬 Conversation memory
* 📡 Streaming responses
* 🐳 Complete Docker Compose deployment
* ☁️ Cloud deployment
* 📊 Observability and monitoring

---

# 🎯 What This Project Demonstrates

This project demonstrates practical implementation of:

```text
Full-Stack Development
        +
Generative AI
        +
Agentic AI
        +
Advanced RAG
        +
Hybrid Search
        +
Reranking
        +
Vector Databases
        +
SQL / PostgreSQL
        +
LLM Tool Calling
        +
LangGraph
        +
FastAPI
        +
React
```

The system connects a modern **React frontend** with a **FastAPI backend** and an **Agentic RAG intelligence layer**, allowing users to interact with enterprise knowledge through a natural-language interface.

---

# 👨‍💻 Author

**Abhishek Kumar Abhi**

GitHub:

https://github.com/AbhishekAbhi71

---

# ⭐ If You Find This Project Interesting

Feel free to explore the repository, raise issues, or contribute improvements.
