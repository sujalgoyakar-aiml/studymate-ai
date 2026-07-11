# studymate-ai
# studymate-ai
#  StudyMate AI

Your personal study assistant — ask any subject or upload a PDF to get explanations, summaries, and quizzes, in any language.


# Features

General Mode** — Ask anything, any subject, no upload needed
Study Mode (PDF)** — Upload your notes/textbook and ask questions grounded in that material
Auto-detects intent** — explain a concept, summarize, generate a quiz, or test you on the material
Multi-language support** — responds in whatever language you ask in
Conversation memory** — keeps recent chat context for follow-up questions


#Built With

[Streamlit](https://streamlit.io/) — web app framework
[Groq](https://groq.com/) — LLM inference (Llama 3.3 70B)
[PyPDF2](https://pypi.org/project/PyPDF2/) — PDF text extraction

# Running Locally

1. Clone this repo:
bash
   git clone https://github.com/YOUR_USERNAME/studymate-ai.git
   cd studymate-ai

2. Install dependencies:
bash
   pip install -r requirements.txt


3. Set your Groq API key as an environment variable:
bash
   export GROQ_API_KEY="your_groq_api_key_here"

   *(On Windows, use set GROQ_API_KEY=your_key_here)*

4. Run the app:
bash
   streamlit run app.py


# Deployment

This app is deployed on [Streamlit Community Cloud](https://share.streamlit.io/). To deploy your own copy:

1. Fork/clone this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub
3. Create a new app, point it to this repo, main file app.py
4. Add GROQ_API_KEY under **Secrets** in the app settings
5. Deploy 


# License

This project is licensed under the MIT License.
