import os
import re
from dotenv import load_dotenv
from llm_router import generate

load_dotenv()

VERIFICATION_CODE = "12345"
SQL_PROMPT = """
You are an expert PostgreSQL query generator.

Database: PostgreSQL

Tables:

products
- product_id
- name
- category
- price
- stock_quantity
- units_sold_last_7_days
- units_sold_last_30_days
- revenue_last_7_days
- revenue_last_30_days

customers
- customer_id
- name
- email
- phone
- created_at

orders
- order_id
- customer_id
- order_date
- amount

order_items
- order_item_id
- order_id
- product_id
- quantity
- price_at_purchase

order_items.order_id → orders.order_id
order_items.product_id → products.product_id

IMPORTANT RULES:
- Generate exactly ONE SQL statement
- Default to SELECT queries only
- NEVER modify data unless the user explicitly provides a verification code
- If the user asks to modify data WITHOUT a verification code, return the text: NEED_VERIFICATION
- Use LIMIT when returning multiple rows
- When searching for product names, ALWAYS use ILIKE with % wildcards.
- Example: WHERE name ILIKE '%pen%'
- NEVER use name = 'pen'
- Return ONLY raw SQL or NEED_VERIFICATION
- Do NOT include any explanations or apologies, just the SQL statement.

Always calculate customer spending using:
SUM(order_items.quantity * order_items.price_at_purchase)

Always group by customer_id and customer name.

Conversation history:
{conversation}

User question:
{question}
"""



def _clean_sql(sql: str) -> str:
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()


def _is_write_query(sql: str) -> bool:
    write_keywords = ["insert", "update", "delete", "drop", "alter", "truncate"]
    return any(word in sql.lower() for word in write_keywords)


def _build_conversation(chat_history: list) -> str:
    """
    Build last few messages into structured conversation context
    """
    if not chat_history:
        return ""

    conversation = ""
    for msg in chat_history[-8:]:  # last 8 messages only
        role = msg.get("role", "").upper()
        content = msg.get("content", "")
        conversation += f"{role}: {content}\n"

    return conversation


def generate_sql(question: str, chat_history: list) -> str:
    conversation = _build_conversation(chat_history)

    prompt = SQL_PROMPT.format(
        conversation=conversation,
        question=question
    )

    raw_output = generate(prompt)

    if raw_output.strip() == "NEED_VERIFICATION":
        raise ValueError(
            "This operation requires verification. "
            "Please re-ask the question including the verification code."
        )

    sql = _clean_sql(raw_output)

    # Block multiple statements
    if ";" in sql.strip()[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Validate SQL starts correctly
    if not re.match(r"^(select|insert|update|delete|drop|alter)", sql.lower()):
        raise ValueError("Invalid SQL generated")

    # Block write queries without verification code
    if _is_write_query(sql) and VERIFICATION_CODE not in question:
        raise ValueError("Write operation blocked. Verification code required.")

    return sql