from app.core.config import settings


async def call_llm(prompt: str) -> dict:
    return {
        "provider": "placeholder",
        "used_api_key": bool(settings.llm_api_key),
        "prompt": prompt,
        "message": "LLM integration not connected yet. Replace this stub with your provider call.",
    }
