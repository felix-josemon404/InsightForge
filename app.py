import streamlit as st
from sql_planner import generate_sql
from sql_executor import execute_sql
from llm import explain_answer
import uuid
import requests
import json
from decimal import Decimal

# =====================================================
# Streamlit Config (MUST BE FIRST STREAMLIT COMMAND)
# =====================================================
st.set_page_config(page_title="Store Analytics Assistant", layout="wide")


# =====================================================
# Safe JSON Serializer (Decimal Fix)
# =====================================================
def serialize_for_json(obj):
    if isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]

    if isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}

    if isinstance(obj, Decimal):
        return float(obj)

    return obj


# =====================================================
# Load or Create Chat Session
# =====================================================
sessions = execute_sql("""
    SELECT session_id, title
    FROM chat_sessions
    ORDER BY created_at DESC;
""")

if "current_chat" not in st.session_state:
    if sessions:
        st.session_state.current_chat = sessions[0]["session_id"]
    else:
        new_id = str(uuid.uuid4())
        execute_sql(f"""
            INSERT INTO chat_sessions (session_id, title)
            VALUES ('{new_id}', 'New Chat');
        """)
        st.session_state.current_chat = new_id


# =====================================================
# Sidebar - Chat List
# =====================================================
st.sidebar.markdown("## 💬 Chats")

if st.sidebar.button("➕ New Chat", key="new_chat_btn"):
    new_id = str(uuid.uuid4())
    execute_sql(f"""
        INSERT INTO chat_sessions (session_id, title)
        VALUES ('{new_id}', 'New Chat');
    """)
    st.session_state.current_chat = new_id
    st.rerun()

sessions = execute_sql("""
    SELECT session_id, title
    FROM chat_sessions
    ORDER BY created_at DESC;
""")

for session in sessions:
    label = session["title"] or session["session_id"][:8]

    if st.sidebar.button(
        label,
        key=f"chat_{session['session_id']}"
    ):
        st.session_state.current_chat = session["session_id"]
        st.rerun()


# =====================================================
# LLM Mode Selector
# =====================================================
st.sidebar.title("⚙️ LLM Settings")

llm_mode = st.sidebar.radio(
    "Choose model",
    options=["auto", "gemini", "local"],
    format_func=lambda x: {
        "auto": "Auto (Gemini → Local fallback)",
        "gemini": "Gemini (Cloud)",
        "local": "Local LLaMA"
    }[x]
)

st.session_state["llm_mode"] = llm_mode


# =====================================================
# Main UI
# =====================================================
st.title("🏪 Store Agent")


# =====================================================
# Display Chat History
# =====================================================
messages = execute_sql(f"""
    SELECT role, content
    FROM chat_messages
    WHERE session_id = '{st.session_state.current_chat}'
    ORDER BY created_at ASC;
""")

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =====================================================
# User Input
# =====================================================
question = st.text_input("Ask a question about your store")

if st.button("Ask", key="ask_btn"):
    try:

        # =================================================
        # FOLLOW-UP: Apply Discount
        # =================================================
        if "them" in question.lower() and "discount" in question.lower():

            context = execute_sql(f"""
                SELECT last_result
                FROM session_context
                WHERE session_id = '{st.session_state.current_chat}';
            """)

            if not context:
                st.error("No previous result in this chat.")
                st.stop()

            last_result = context[0]["last_result"]
            customers_payload = []

            for row in last_result:
                cid = row.get("customer_id")
                name = row.get("name")
                email = row.get("email")

                if not cid:
                    continue

                execute_sql(f"""
                    INSERT INTO customer_discounts (
                        customer_id,
                        discount_percentage,
                        valid_until
                    )
                    VALUES (
                        {cid},
                        10,
                        CURRENT_TIMESTAMP + INTERVAL '30 days'
                    );
                """)

                customers_payload.append({
                    "customer_id": cid,
                    "name": name,
                    "email": email
                })

            webhook_url = "http://localhost:5678/webhook/top-discount"

            requests.post(
                webhook_url,
                json={
                    "discount": 10,
                    "valid_days": 30,
                    "customers": customers_payload
                }
            )

            execute_sql(f"""
                INSERT INTO chat_messages (session_id, role, content)
                VALUES (
                    '{st.session_state.current_chat}',
                    'assistant',
                    '10% discount applied and emails triggered.'
                );
            """)

            st.success("10% discount applied and emails triggered.")
            st.rerun()


        # =================================================
        # NORMAL QUESTION FLOW
        # =================================================
        # =================================================
        # NORMAL QUESTION FLOW
        # =================================================

        # Get previous conversational result
        context = execute_sql(f"""
            SELECT last_result
            FROM session_context
            WHERE session_id = '{st.session_state.current_chat}';
        """)

        previous_result = context[0]["last_result"] if context else None

        sql = generate_sql(question, previous_result)
        data = execute_sql(sql)

        clean_data = serialize_for_json(data)

        answer = explain_answer(question, sql, data, messages)        

        # Store user message
        execute_sql(f"""
            INSERT INTO chat_messages (session_id, role, content)
            VALUES (
                '{st.session_state.current_chat}',
                'user',
                '{question.replace("'", "''")}'
            );
        """)

        # Auto-update chat title if still default
        current_title = execute_sql(f"""
            SELECT title
            FROM chat_sessions
            WHERE session_id = '{st.session_state.current_chat}';
        """)[0]["title"]

        if current_title == "New Chat":
            short_title = question.strip().capitalize()[:40].replace("'", "''")
            execute_sql(f"""
                UPDATE chat_sessions
                SET title = '{short_title}'
                WHERE session_id = '{st.session_state.current_chat}';
            """)

        # Store assistant message
        execute_sql(f"""
            INSERT INTO chat_messages (session_id, role, content)
            VALUES (
                '{st.session_state.current_chat}',
                'assistant',
                '{answer.replace("'", "''")}'
            );
        """)

        # Store last_result persistently
        execute_sql(f"""
            INSERT INTO session_context (session_id, last_result)
            VALUES (
                '{st.session_state.current_chat}',
                '{json.dumps(clean_data)}'
            )
            ON CONFLICT (session_id)
            DO UPDATE SET
                last_result = EXCLUDED.last_result,
                updated_at = CURRENT_TIMESTAMP;
        """)

        st.rerun()

    except Exception as e:
        st.error(str(e))