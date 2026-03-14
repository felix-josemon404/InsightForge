import os
import google.generativeai as genai
from dotenv import load_dotenv
import ollama
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_MODEL = os.getenv("model_name", "gemini-1.5-flash")
LLAMA_MODEL = "llama3-chatqa:8b"


def generate(prompt: str) -> str:
    """
    LLM router controlled by UI:
    - auto   → Gemini, fallback to LLaMA
    - gemini → Gemini only
    - local  → LLaMA only
    """

    mode = st.session_state.get("llm_mode", "auto")

    # ---------- FORCE LOCAL ----------
    if mode == "local":
        return _run_llama(prompt)

    # ---------- FORCE GEMINI ----------
    if mode == "gemini":
        return _run_gemini(prompt)

    # ---------- AUTO MODE ----------
    try:
        return _run_gemini(prompt)
    except Exception as e:
        print("⚠️ Gemini failed, auto-fallback to LLaMA:", e)
        return _run_llama(prompt)


def _run_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()


def _run_llama(prompt: str) -> str:
    response = ollama.chat(
        model=LLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()
