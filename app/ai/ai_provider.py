import requests

from app.config import LLM_API_KEY, LLM_MODEL

class GroqProvider:
    BASE_URL = "https://api.groq.com/openai/v1"

    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or LLM_API_KEY
        self.model = model or LLM_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt: str) -> str:
        url = f"{self.BASE_URL}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0
        }

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]