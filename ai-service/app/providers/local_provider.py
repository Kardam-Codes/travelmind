import json
import os
from urllib import error, request

from providers.base import LLMProvider


class LocalLLMProvider(LLMProvider):
    provider_name = "ollama-local"

    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:11434")
        self.model_name = os.getenv("LOCAL_LLM_MODEL", "llama3.2:3b")
        self.timeout_seconds = int(os.getenv("LOCAL_LLM_TIMEOUT_SECONDS", "90"))
        self.system_prompt = os.getenv(
            "LOCAL_LLM_SYSTEM_PROMPT",
            (
                "You extract travel intent into one JSON object. "
                "Do not explain. Do not add markdown. Do not invent places. "
                "Use only the provided cities, preference tags, and traveler types."
            ),
        )

    def generate_json(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model_name,
                "prompt": prompt,
                "system": self.system_prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                    "top_p": 0.1,
                    "num_predict": 220,
                },
            }
        ).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except (TimeoutError, error.URLError, error.HTTPError, OSError, json.JSONDecodeError) as exc:
            raise RuntimeError("Local LLM provider is unavailable.") from exc

        return response_data.get("response", "")
