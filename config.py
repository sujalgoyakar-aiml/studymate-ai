"""
config.py — Loads secrets and creates the Groq client.
Nothing else in the app should touch os.environ or st.secrets directly.
"""

import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
