from app.features.ai.llm_client import call_llm
from app.features.ai.prompt_builder import build_trip_extraction_prompt


async def extract_trip_intent(user_input: str) -> dict:
    prompt = build_trip_extraction_prompt(user_input)
    return await call_llm(prompt)
