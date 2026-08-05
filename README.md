# StudyMate AI 📚

> Your personal AI study assistant — upload any PDF and ask questions in any language.

🚀 **Live Demo:** https://studymate-ai-3hk33gaescaqiqkxqrqdtm.streamlit.app/

---

## What It Does

StudyMate AI is a deployed web application that acts as a personal study assistant for any student — BTech, medical, law, CA, UPSC, school — any subject, any field, any language.

### Two Modes

**📄 Study Mode (PDF)**
- Upload any PDF — textbook, notes, syllabus
- AI reads your material and answers questions from it
- Auto-detects what you need — explain, summarize, quiz, test

**🌐 General Mode**
- Ask anything without uploading a PDF
- Live web search for current events and real-time information
- Coding, law, medicine, finance — any topic

---

## Key Features

- **RAG Pipeline** — retrieves relevant PDF chunks before answering, not entire document
- **Auto Intent Detection** — detects if you want explanation, summary, quiz, or test from your question
- **Live Web Search** — DuckDuckGo integration for real-time information
- **Conversation Memory** — remembers last 3 exchanges for context
- **Multi-language Support** — auto-detects and responds in student's language
- **Secure API** — Groq API key stored in environment variables, never in code
- ---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main language |
| Streamlit | Web UI framework |
| Groq API | LLM access (free) |
| LLaMA 3.3 70B | AI model |
| PyPDF2 | PDF text extraction |
| DuckDuckGo Search | Live web search |
| Streamlit Cloud | Deployment |

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/sujalgoyakar-aiml/studymate-ai

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY=your_groq_key_here

# Run the app
streamlit run app.py
```

---

## What I Learned

- RAG (Retrieval Augmented Generation) pipeline implementation
- Prompt engineering for auto intent detection
- Groq API and LLaMA model integration
- Streamlit session state management
- Secure environment variable handling
- Streamlit Cloud deployment

---

## Project Structure


---

## How It Works
