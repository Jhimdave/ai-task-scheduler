from dotenv import load_dotenv
import os

load_dotenv()

# Todoist
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")

# AI Providers
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Webhook
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # Optional

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

if not TODOIST_API_KEY:
    raise ValueError("TODOIST_API_KEY not set")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")