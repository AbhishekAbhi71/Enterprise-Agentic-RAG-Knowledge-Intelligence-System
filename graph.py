from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model

from config import CLEANED_GEMINI_KEY
from tools import tools

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=CLEANED_GEMINI_KEY,
)

router_llm = llm.bind_tools(tools)
tool_node = ToolNode(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_query: str
    final_ans: str

SYSTEM_PROMPT = """
You are the routing agent of an Enterprise Agentic RAG system.

Your job is to select exactly ONE tool that should be used
to answer the user's query.

Available tools:

1. rag_route
Use this when the answer comes from company documents,
policies, handbooks, PDFs, or other unstructured documents.

Examples:
- What is the maximum hotel reimbursement per night?
- Who owns the Remote Work Policy?
- How often must passwords be changed?
- Who must approve international travel?

2. sql_route
Use this when the answer requires structured information
from PostgreSQL.

Examples:
- How many employees are in the Finance department?
- What is the average salary in Engineering?
- Which employees have more than 5 years of service?
- How many employees joined after 2023?

3. hybrid_route
Use this when BOTH document information and PostgreSQL
information are required.

Examples:
- According to the leave policy, how many employees are
eligible for 30 days of annual leave?
- Which employees qualify for pension contributions
according to company policy?

IMPORTANT:

Do not select a tool merely because of words such as
"what", "who", "how many", or "which".

Understand what information is actually required.

You MUST call exactly ONE of the available tools.

Do not answer the user's question yourself.
Select the appropriate tool and pass the ORIGINAL user
query to it.
"""

def query_analyzer(state: AgentState) -> AgentState:
    user_query = state["user_query"]

    response = router_llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ])

    return {
        **state,
        "messages": [response],
    }

def answer_generator(state: AgentState) -> AgentState:
    user_query = state["user_query"]
    messages = state["messages"]
    evidence = messages[-1].content

    prompt = f"""
You are the answer generator of an Enterprise Agentic RAG system.
Answer the user's question using ONLY the evidence returned
by the selected tool.

User Question: {user_query}
Evidence: {evidence}

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. Give a clear and concise answer.
4. If the evidence contains document information,
   mention the relevant policy/source.
5. If the evidence contains database information,
   mention that the result came from PostgreSQL.
6. For hybrid queries, combine the document rule and
   database result logically.
"""

    response = llm.invoke(prompt)
    answer = response.content

    return {
        **state,
        "final_ans": answer,
    }

def verifier(state: AgentState) -> AgentState:
    user_query = state["user_query"]
    answer = state["final_ans"]
    messages = state["messages"]
    evidence = messages[-1].content

    prompt = f"""
You are the final answer verification agent.

Return ONLY the final answer to the user's question.
Do not describe whether the draft is supported.
Do not say "the answer is supported".
Do not mention this verification task.

User question:
{user_query}

Evidence:
{evidence}

Draft answer:
{answer}

Rules:
1. Preserve claims supported by the evidence.
2. Remove unsupported claims.
3. Do not add outside knowledge.
4. Answer the user's question directly.
5. Mention the document source or PostgreSQL when available.
6. If the evidence is insufficient, say:
   "The available evidence is insufficient to answer this."
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "final_ans": response.content.strip(),
    }

builder = StateGraph(AgentState)

builder.add_node("query_analyzer", query_analyzer)
builder.add_node("tools", tool_node)
builder.add_node("answer_generator", answer_generator)
builder.add_node("verifier", verifier)

builder.add_edge(START, "query_analyzer")
builder.add_conditional_edges(
    "query_analyzer",
    tools_condition,
    {"tools": "tools", END: END},
)

builder.add_edge("tools", "answer_generator")
builder.add_edge("answer_generator", "verifier")
builder.add_edge("verifier", END)

graph = builder.compile()

def run_query(user_query: str) -> str:
    result = graph.invoke({
        "messages": [],
        "user_query": user_query,
        "final_ans": "",
    })
    return result["final_ans"]