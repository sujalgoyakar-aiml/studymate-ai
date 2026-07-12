import streamlit as st
import PyPDF2
import os
from groq import Groq
from duckduckgo_search import DDGS

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="StudyMate AI", page_icon="📚", layout="centered")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background-color: #0f0f0f; }
.block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 2rem; }
.main-title { font-size: 1.8rem; font-weight: 700; color: #ffffff; text-align: center; margin-bottom: 0.2rem; }
.main-subtitle { font-size: 0.85rem; color: #6b6b6b; text-align: center; margin-bottom: 2rem; }
.stChatMessage { background-color: transparent !important; border: none !important; }
[data-testid="stChatMessageContent"] { background-color: #1a1a1a; border-radius: 12px; padding: 12px 16px; color: #e0e0e0; font-size: 0.95rem; line-height: 1.6; border: 1px solid #2a2a2a; }
textarea[data-testid="stChatInputTextArea"] { background-color: #1a1a1a !important; border: 1px solid #333 !important; border-radius: 12px !important; color: #e0e0e0 !important; }
[data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
[data-testid="stSidebar"] * { color: #c0c0c0 !important; }
[data-testid="stFileUploader"] { background-color: #1a1a1a; border: 1px dashed #333; border-radius: 10px; padding: 1rem; }
.stButton button { background-color: #1a1a1a !important; border: 1px solid #333 !important; color: #c0c0c0 !important; border-radius: 8px !important; width: 100% !important; }
.stButton button:hover { background-color: #252525 !important; }
.mode-badge { display: block; background-color: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 20px; padding: 4px 12px; font-size: 0.78rem; color: #888; text-align: center; width: fit-content; margin: 0 auto 1.5rem auto; }
.welcome-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 1.5rem 0; }
.welcome-card { background-color: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 10px; padding: 14px; font-size: 0.82rem; color: #888; }
.welcome-card strong { color: #c0c0c0; display: block; margin-bottom: 4px; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

for key, val in [("messages",[]),("pdf_text",""),("pdf_loaded",False)]:
    if key not in st.session_state:
        st.session_state[key] = val

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Settings")
    st.markdown("---")
    mode = st.radio("Mode", ["🌐 General", "📄 Study (PDF)"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = None
    if "Study" in mode:
        st.markdown("**Upload Material**")
        uploaded_file = st.file_uploader("PDF only", type="pdf", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.update({"messages":[], "pdf_text":"", "pdf_loaded":False})
        st.rerun()
    st.markdown("---")
    if "Study" in mode:
        st.markdown("<div style='font-size:0.78rem;color:#555'>Upload any PDF and ask questions from it</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.78rem;color:#555'>Ask anything — coding, law, medicine, current events</div>", unsafe_allow_html=True)

st.markdown('<p class="main-title">📚 StudyMate</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Your personal AI study assistant</p>', unsafe_allow_html=True)
mode_label = "🌐 General Mode — web search enabled" if "General" in mode else "📄 Study Mode — answers from your PDF"
st.markdown(f'<div class="mode-badge">{mode_label}</div>', unsafe_allow_html=True)

def extract_pdf(f):
    return "".join(p.extract_text() for p in PyPDF2.PdfReader(f).pages)

def get_relevant(text, q, chunk=500):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk]) for i in range(0, len(words), chunk)]
    matched = [c for c in chunks if any(w.lower() in c.lower() for w in q.split())]
    return "\n\n".join(matched[:3]) if matched else text[:2000]

def needs_web_search(question):
    keywords = ["who is","current","latest","now","today","2024","2025","2026",
                "commissioner","minister","officer","appointed","recently","news",
                "price","rate","score","result","winner","election","ceo","head"]
    return any(kw in question.lower() for kw in keywords)

def web_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n\n".join([f"{r['title']}\n{r['body']}" for r in results])
    except:
        pass
    return ""

def ask_ai(question, history, pdf_text="", use_pdf=False):
    users = [m for m in history if m["role"]=="user"][-3:]
    bots = [m for m in history if m["role"]=="assistant"][-3:]
    hist = "\n".join([f"Student: {u['content']}\nStudyMate: {b['content']}" for u,b in zip(users,bots)])

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

    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=1000
    ).choices[0].message.content

def show_welcome(use_pdf=False):
    if use_pdf:
        st.markdown("""
<div class="welcome-grid">
<div class="welcome-card"><strong>📖 Explain</strong>Ask "What is [topic]?" for simple explanation</div>
<div class="welcome-card"><strong>📝 Summarize</strong>Say "Summarize this" for bullet points</div>
<div class="welcome-card"><strong>❓ Quiz</strong>Say "Quiz me" for 5 practice questions</div>
<div class="welcome-card"><strong>🎯 Test</strong>Say "Test me" for interactive testing</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="welcome-grid">
<div class="welcome-card"><strong>💻 Coding</strong>Python, DSA, web dev concepts</div>
<div class="welcome-card"><strong>⚖️ Law & CA</strong>Legal concepts, tax, finance</div>
<div class="welcome-card"><strong>🔬 Science</strong>Medical, physics, chemistry</div>
<div class="welcome-card"><strong>🌐 Current Events</strong>Latest news, who is in office</div>
</div>""", unsafe_allow_html=True)

def chat_ui(use_pdf=False):
    if not st.session_state.messages:
        show_welcome(use_pdf)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    placeholder = "Ask about your material..." if use_pdf else "Ask me anything..."
    if q := st.chat_input(placeholder):
        st.session_state.messages.append({"role":"user","content":q})
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            with st.spinner(""):
                ans = ask_ai(q, st.session_state.messages, st.session_state.pdf_text, use_pdf)
            st.write(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})

if "Study" in mode:
    if not uploaded_file:
        st.markdown("""
<div style='text-align:center;padding:3rem 0;color:#555'>
<div style='font-size:2rem;margin-bottom:1rem'>📄</div>
<div style='font-size:0.95rem'>Upload your study material from the sidebar</div>
<div style='font-size:0.8rem;color:#444;margin-top:0.5rem'>Supports any PDF — textbooks, notes, syllabus</div>
</div>""", unsafe_allow_html=True)
    else:
        if not st.session_state.pdf_loaded:
            with st.spinner("Reading your PDF..."):
                st.session_state.pdf_text = extract_pdf(uploaded_file)
                st.session_state.pdf_loaded = True
            st.success(f"Ready — {len(st.session_state.pdf_text):,} characters loaded")
        chat_ui(use_pdf=True)
else:
    chat_ui(use_pdf=False)
