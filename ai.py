"""
ai.py — Builds the prompt (PDF-grounded or general+web-search) and calls the LLM.
"""

from config import client, MODEL
from pdf_utils import get_relevant
from search import needs_web_search, web_search


def _build_history_text(history: list) -> str:
    users = [m for m in history if m["role"] == "user"][-3:]
    bots = [m for m in history if m["role"] == "assistant"][-3:]
    return "\n".join([f"Student: {u['content']}\nStudyMate: {b['content']}" for u, b in zip(users, bots)])


def ask_ai(question: str, history: list, pdf_text: str = "", use_pdf: bool = False) -> str:
    hist = _build_history_text(history)

    if use_pdf:
        prompt = f"""You are StudyMate AI tutor. Use ONLY this material:
{get_relevant(pdf_text, question)}

Chat history: {hist}
Student: {question}

Detect intent automatically:
- explain/what is -> clear explanation with examples
- summarize -> structured bullet points
- quiz -> 5 Q&A with answers
- test me -> ask 1 question
- answering -> evaluate response
- else -> answer clearly

Respond in student language. If not in material, say so."""
    else:
        search_context = ""
        if needs_web_search(question):
            results = web_search(question)
            if results:
                search_context = f"LIVE SEARCH RESULTS:\n{results}\n\n"
        prompt = f"""You are StudyMate, helpful AI for students worldwide.

{search_context}Chat history: {hist}
Question: {question}

Answer clearly and accurately.
Use search results as primary source when available.
If unsure about any fact, say so honestly.
Respond in student language automatically."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return response.choices[0].message.content
