import streamlit as st
import PyPDF2
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="StudyMate AI", page_icon="📚", layout="wide")
st.title("📚 StudyMate AI")
st.caption("Your Personal Study Assistant — Any Subject, Any Language")

for key, val in [("messages",[]),("pdf_text",""),("pdf_loaded",False)]:
    if key not in st.session_state:
        st.session_state[key] = val

with st.sidebar:
    mode = st.radio("Mode:", ["🌐 General Mode", "📄 Study Mode (PDF)"])
    uploaded_file = st.file_uploader("Upload PDF", type="pdf") if "Study" in mode else None
    if st.button("Clear Chat"):
        st.session_state.update({"messages":[], "pdf_text":"", "pdf_loaded":False})
        st.rerun()
    st.markdown("---")
    examples = "- What is data mining?\n- Summarize this\n- Quiz me\n- Test me" if "Study" in mode else "- Explain Python loops\n- What is tort law?\n- How does heart work?"
    st.markdown(f"**Examples:**\n{examples}")

def extract_pdf(f):
    return "".join(p.extract_text() for p in PyPDF2.PdfReader(f).pages)

def get_relevant(text, q, chunk=500):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk]) for i in range(0, len(words), chunk)]
    matched = [c for c in chunks if any(w.lower() in c.lower() for w in q.split())]
    return "\n\n".join(matched[:3]) if matched else text[:2000]

def ask_ai(question, history, pdf_text="", use_pdf=False):
    users = [m for m in history if m["role"]=="user"][-3:]
    bots = [m for m in history if m["role"]=="assistant"][-3:]
    hist = "\n".join([f"Student: {u['content']}\nStudyMate: {b['content']}" for u,b in zip(users,bots)])
    
    if use_pdf:
        prompt = f"""You are StudyMate AI tutor. Use ONLY this material to answer:
{get_relevant(pdf_text, question)}

Previous chat: {hist}
Student: {question}

Auto-detect what student needs:
- explain/what is → simple explanation with real examples
- summarize → structured bullet points
- quiz/questions → 5 Q&A with answers
- test me → ask 1 question only
- if answering → evaluate their response
- else → answer clearly

Respond in same language as student.
If topic not in material, say so honestly."""
    else:
        prompt = f"""You are StudyMate, helpful AI for students worldwide.
Previous chat: {hist}
Question: {question}
Answer any topic clearly. Respond in student's language automatically."""

    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=1000
    ).choices[0].message.content

def chat_ui(use_pdf=False):
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    placeholder = "Ask about your material..." if use_pdf else "Ask anything..."
    if q := st.chat_input(placeholder):
        st.session_state.messages.append({"role":"user","content":q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = ask_ai(q, st.session_state.messages, st.session_state.pdf_text, use_pdf)
            st.write(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})

if "Study" in mode:
    if not uploaded_file:
        st.info("Upload a PDF in the sidebar to get started.")
    else:
        if not st.session_state.pdf_loaded:
            with st.spinner("Reading PDF..."):
                st.session_state.pdf_text = extract_pdf(uploaded_file)
                st.session_state.pdf_loaded = True
            st.success(f"PDF loaded — {len(st.session_state.pdf_text)} characters.")
        chat_ui(use_pdf=True)
else:
    st.info("General Mode — Ask anything, no PDF needed!")
    chat_ui(use_pdf=False)
