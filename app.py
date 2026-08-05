"""
app.py — UI layer only. Logic lives in ai.py, pdf_utils.py, search.py.
Run locally with: streamlit run app.py
"""

import streamlit as st
from ai import ask_ai
from pdf_utils import extract_pdf
from styles import STUDYMATE_CSS

st.set_page_config(page_title="StudyMate AI", page_icon="📚", layout="centered")
st.markdown(STUDYMATE_CSS, unsafe_allow_html=True)

for key, val in [("messages", []), ("pdf_text", ""), ("pdf_loaded", False)]:
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
        st.session_state.update({"messages": [], "pdf_text": "", "pdf_loaded": False})
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
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            with st.spinner(""):
                ans = ask_ai(q, st.session_state.messages, st.session_state.pdf_text, use_pdf)
            st.write(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})


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
