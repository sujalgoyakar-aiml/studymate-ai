"""
styles.py — All CSS for the app lives here, as a single string.
"""

STUDYMATE_CSS = """
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
"""
