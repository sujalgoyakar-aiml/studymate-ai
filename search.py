"""
search.py — Decides when a question needs live web search, and runs it.
"""

from duckduckgo_search import DDGS

SEARCH_TRIGGER_KEYWORDS = [
    "who is", "current", "latest", "now", "today", "2024", "2025", "2026",
    "commissioner", "minister", "officer", "appointed", "recently", "news",
    "price", "rate", "score", "result", "winner", "election", "ceo", "head",
]


def needs_web_search(question: str) -> bool:
    """Simple keyword-based check for whether a question likely needs current info."""
    return any(kw in question.lower() for kw in SEARCH_TRIGGER_KEYWORDS)


def web_search(query: str, max_results: int = 3) -> str:
    """Runs a DuckDuckGo search and returns formatted title+body results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if results:
                return "\n\n".join([f"{r['title']}\n{r['body']}" for r in results])
    except Exception:
        pass
    return ""
