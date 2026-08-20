import requests
from google import genai
from google.genai import errors

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
        enable_fallback: bool = True,
    ):
        self.provider = ai_model.lower()
        self.enable_fallback = enable_fallback

        if self.provider not in self.PROVIDERS:
            raise ValueError(
                f"Unsupported AI provider: {self.provider}"
            )

        config = self.PROVIDERS[self.provider]

        self.api_key = config["api_key"]
        self.model = model or config["model"]

        if not self.api_key:
            raise ValueError(
                f"{self.provider.upper()} API key not configured."
            )

        # Initialize Groq
        if self.provider == "groq":
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

        # Initialize Gemini
        elif self.provider == "gemini":
            self.client = genai.Client(
                api_key=self.api_key
            )

    def generate(self, prompt: str) -> str:

        # =========================
        # GEMINI
        # =========================
        if self.provider == "gemini":

            try:
                return self._generate_gemini(prompt)

            except Exception as e:

                # Gemini failed
                print(
                    f"[Gemini] Request failed: {type(e).__name__}: {e}"
                )

                # Try Groq fallback
                if self.enable_fallback:
                    print(
                        "[AIProvider] Switching from Gemini to Groq..."
                    )

                    return self._generate_groq_fallback(prompt)

                raise

        # =========================
        # GROQ
        # =========================
        if self.provider == "groq":
            return self._generate_groq(prompt)

        raise ValueError(
            f"Unsupported AI provider: {self.provider}"
        )

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

        if not GROQ_API_KEY:
            raise RuntimeError(
                "Gemini failed and GROQ_API_KEY is not configured."
            )

        # Use the Groq credentials
        groq_headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": GROQ_MODEL,
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
            headers=groq_headers,
            timeout=30,
        )

        response.raise_for_status()

        print(
            f"[AIProvider] Groq fallback successful "
            f"using model: {GROQ_MODEL}"
        )

        return response.json()["choices"][0]["message"]["content"]

    def _generate_gemini(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0,
                "response_mime_type": "application/json",
            },
        )

        return response.text