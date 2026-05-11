import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(" Missing GROQ_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(" Missing TAVILY_API_KEY")