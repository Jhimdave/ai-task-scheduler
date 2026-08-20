import requests
from google import genai
from google.api_core import exceptions as google_exceptions

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
)


class AIProvider:
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"

    PROVIDERS = {
        "groq": {
            "api_key": GROQ_API_KEY,
            "model": GROQ_MODEL,
        },
        "gemini": {
            "api_key": GEMINI_API_KEY,
            "model": GEMINI_MODEL,
        },
    }

    def __init__(
        self,
        ai_model: str = "groq",
        model: str | None = None,
    ):
        self.provider = ai_model.lower()
        self.fallback_provider = None

        if self.provider not in self.PROVIDERS:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

        config = self.PROVIDERS[self.provider]

        self.api_key = config["api_key"]
        self.model = model or config["model"]

        if not self.api_key:
            raise ValueError(f"{self.provider.upper()} API key not configured.")

        if self.provider == "groq":
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

        elif self.provider == "gemini":
            self.client = genai.Client(api_key=self.api_key)
            # Setup fallback to Groq for Gemini
            self._setup_fallback()

    def _setup_fallback(self):
        """Setup fallback provider (Groq) for Gemini."""
        if self.provider == "gemini" and self.PROVIDERS["groq"]["api_key"]:
            groq_config = self.PROVIDERS["groq"]
            self.fallback_provider = {
                "name": "groq",
                "api_key": groq_config["api_key"],
                "model": groq_config["model"],
                "headers": {
                    "Authorization": f"Bearer {groq_config['api_key']}",
                    "Content-Type": "application/json",
                },
            }

    def generate(self, prompt: str) -> str:
        if self.provider == "groq":
            return self._generate_groq(prompt)

        if self.provider == "gemini":
            return self._generate_gemini(prompt)

        raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _generate_groq(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "response_format": {
                "type": "json_object",
            },
            "temperature": 0,
        }

        response = requests.post(
            f"{self.GROQ_BASE_URL}/chat/completions",
            json=payload,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    def _generate_groq_fallback(self, prompt: str) -> str:
        """Generate response using Groq as fallback provider."""
        payload = {
            "model": self.fallback_provider["model"],
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "response_format": {
                "type": "json_object",
            },
            "temperature": 0,
        }

        response = requests.post(
            f"{self.GROQ_BASE_URL}/chat/completions",
            json=payload,
            headers=self.fallback_provider["headers"],
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    def _generate_gemini(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": 0,
                    "response_mime_type": "application/json",
                },
            )
            return response.text
        except (
            google_exceptions.ResourceExhausted,
            google_exceptions.ServiceUnavailable,
            google_exceptions.DeadlineExceeded,
        ) as e:
            if self.fallback_provider:
                print(
                    f"Gemini quota exceeded or unavailable: {e}. "
                    f"Falling back to {self.fallback_provider['name'].upper()}..."
                )
                return self._generate_groq_fallback(prompt)
            raise