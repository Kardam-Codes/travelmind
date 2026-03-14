import json
import os
from urllib import error, request

from providers.base import LLMProvider


class LocalLLMProvider(LLMProvider):
    provider_name = "ollama-local"

    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:11434")
        self.model_name = os.getenv("LOCAL_LLM_MODEL", "llama3.2:3b")

    def generate_json(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            }
        ).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=20) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except error.URLError as exc:
            raise RuntimeError("Local LLM provider is unavailable.") from exc

        return response_data.get("response", "")
