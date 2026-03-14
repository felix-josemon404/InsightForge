from llm_router import generate


def explain_answer(question: str, sql: str, data: list, chat_history: list):
    conversation = ""

    for msg in chat_history[-6:]:  # last few messages only
        conversation += f"{msg['role'].upper()}: {msg['content']}\n"

    prompt = f"""
You are a store analytics assistant.

IMPORTANT RULES:

- Use ONLY the QUERY RESULT to answer.
- Do NOT use outside knowledge.
- Do NOT guess.
- If result is empty say: "No data found".

- If there are MULTIPLE rows in QUERY RESULT,
  list ALL rows clearly.

Example:

QUERY RESULT:
[
 {{"name":"Ballpoint Pen (Blue)","price":0.6}}
 {{"name":"Fountain Pen","price":24.0}}
]

Answer:
Ballpoint Pen (Blue) costs 0.6 and Fountain Pen costs 24.0.


-Never return only one value when multiple rows exist.
-Always include the product name with the price.

Conversation so far:
{conversation}

SQL QUERY:
{sql}

QUERY RESULT:
{data}

Current Question:
{question}

Answer clearly and accurately.
"""

    return generate(prompt)

