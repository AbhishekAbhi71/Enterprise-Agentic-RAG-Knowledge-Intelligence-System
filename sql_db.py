import re
from sqlalchemy import create_engine, text
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_classic.chains.sql_database.query import create_sql_query_chain

from config import POSTGRES_URL, CLEANED_GEMINI_KEY
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=CLEANED_GEMINI_KEY,
)

engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
db = SQLDatabase(engine)

sql_chain = create_sql_query_chain(llm, db)

def clean_sql(sql_query: str) -> str:
    sql_query = str(sql_query).strip()
    sql_query = re.sub(r"```(?:sql)?", "", sql_query, flags=re.IGNORECASE)
    sql_query = re.sub(r"^\s*SQLQuery\s*:\s*", "", sql_query, flags=re.IGNORECASE)
    sql_query = re.sub(r"^\s*SQL\s*Query\s*:\s*", "", sql_query, flags=re.IGNORECASE)

    match = re.search(r"\b(SELECT|WITH)\b", sql_query, flags=re.IGNORECASE)
    if match:
        sql_query = sql_query[match.start():]

    return sql_query.strip().rstrip(";").strip()

def run_sql_query(user_question: str) -> dict:
    generated_sql = sql_chain.invoke({"question": user_question})
    generated_sql = clean_sql(generated_sql)

    normalized_sql = generated_sql.lower().lstrip()
    if not normalized_sql.startswith(("select", "with")):
        raise ValueError(
            "Only read-only SELECT/WITH queries are allowed.\n"
            f"Generated SQL: {generated_sql}"
        )

    with engine.connect() as connection:
        result = connection.execute(text(generated_sql))
        rows = [dict(row._mapping) for row in result]

    return {
        "sql_query": generated_sql,
        "database_rows": rows,
    }