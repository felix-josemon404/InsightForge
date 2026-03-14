import json
from dotenv import load_dotenv
from llm_router import generate


load_dotenv()

PLANNER_PROMPT = """
You are a data query planner for a retail analytics system.

Available table: products

Available columns:
- product_id
- name
- category
- price
- stock_quantity
- units_sold_last_7_days
- units_sold_last_30_days
- revenue_last_7_days
- revenue_last_30_days

Your job:
- Decide what data should be queried from PostgreSQL
- Do NOT calculate values
- Do NOT explain anything
- ONLY return valid JSON

JSON format (return exactly this structure):
{
  "query_type": "top_sales | low_stock | revenue_summary | product_lookup",
  "time_window": "7_days | 30_days | none",
  "limit": number
}

User question:
{question}
"""


def plan_query(question: str) -> dict:
    prompt = PLANNER_PROMPT.format(question=question)
    response = generate(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "query_type": "top_sales",
            "time_window": "30_days",
            "limit": 5
        }
