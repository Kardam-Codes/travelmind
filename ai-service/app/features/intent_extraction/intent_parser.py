"""
Feature: Intent Extraction
File Purpose: Extract travel parameters from user input
Owner: Yug
Dependencies: Local LLM provider
Last Updated: 2026-03-14
"""
import json
import os

from pydantic import BaseModel, Field, ValidationError

from providers.heuristic_provider import HeuristicProvider
from providers.local_provider import LocalLLMProvider


class ExtractIntentResponse(BaseModel):
    destination_city: str | None = None
    unsupported_city: str | None = None
    duration_days: int | None = None
    budget_total: float | None = None
    budget_level: str | None = None
    preferences: list[str] = Field(default_factory=list)
    traveler_type: str | None = None
    confidence: float = 0.0
    missing_fields: list[str] = Field(default_factory=list)
    raw_reasoning_summary: str | None = None
    normalized_query: str
    provider: str = "heuristic-fallback"


class IntentParser:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompt_path = os.path.join(current_dir, "..", "..", "prompts", "trip_prompt.txt")
        self.local_provider = LocalLLMProvider()
        self.fallback_provider = HeuristicProvider()

    def parse_user_intent(
        self,
        user_query: str,
        supported_cities: list[str],
        allowed_preference_tags: list[str],
        allowed_traveler_types: list[str],
    ) -> ExtractIntentResponse:
        with open(self.prompt_path, "r", encoding="utf-8") as file:
            template = file.read()

        formatted_prompt = (
            template.replace("{UserQuery}", user_query)
            .replace("{SupportedCities}", ", ".join(supported_cities))
            .replace("{AllowedPreferenceTags}", ", ".join(allowed_preference_tags))
            .replace("{AllowedTravelerTypes}", ", ".join(allowed_traveler_types))
        )

        for provider in (self.local_provider, self.fallback_provider):
            try:
                raw_response = provider.generate_json(formatted_prompt)
                parsed = ExtractIntentResponse.model_validate(json.loads(raw_response))
                parsed.provider = provider.provider_name
                return _post_process(parsed, supported_cities, allowed_preference_tags, allowed_traveler_types)
            except (RuntimeError, TimeoutError, OSError, json.JSONDecodeError, ValidationError):
                continue

        fallback = ExtractIntentResponse(
            normalized_query=user_query.strip(),
            missing_fields=["destination_city", "duration_days"],
            raw_reasoning_summary="No extraction provider produced a valid response.",
        )
        return fallback


def _post_process(
    parsed: ExtractIntentResponse,
    supported_cities: list[str],
    allowed_preference_tags: list[str],
    allowed_traveler_types: list[str],
) -> ExtractIntentResponse:
    if parsed.destination_city and parsed.destination_city not in supported_cities:
        parsed.unsupported_city = parsed.destination_city
        parsed.destination_city = None
    parsed.preferences = [tag for tag in parsed.preferences if tag in allowed_preference_tags]
    if parsed.traveler_type not in allowed_traveler_types:
        parsed.traveler_type = None

    missing_fields = []
    if not parsed.destination_city:
        missing_fields.append("destination_city")
    if parsed.duration_days is None:
        missing_fields.append("duration_days")
    parsed.missing_fields = missing_fields
    return parsed
