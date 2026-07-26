from dotenv import load_dotenv
import os

load_dotenv()

TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

if not TODOIST_API_KEY:
    raise ValueError("TODOIST_API_KEY not set")

if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY not set")