"""
pdf_utils.py — PDF text extraction and simple relevance-based chunk retrieval.
"""

import PyPDF2


def extract_pdf(f):
    """Extracts all text from an uploaded PDF file object."""
    return "".join(p.extract_text() for p in PyPDF2.PdfReader(f).pages)


def get_relevant(text: str, question: str, chunk: int = 500):
    """
    Splits the PDF text into word-count chunks and returns the chunks
    that contain any word from the question — a simple keyword-based
    retrieval step (not embeddings/vector search).
    """
    words = text.split()
    chunks = [" ".join(words[i:i + chunk]) for i in range(0, len(words), chunk)]
    matched = [c for c in chunks if any(w.lower() in c.lower() for w in question.split())]
    return "\n\n".join(matched[:3]) if matched else text[:2000]
