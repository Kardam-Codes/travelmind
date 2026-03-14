from typing import List

import httpx

from app.core.config import settings
from app.schemas.ai import (
    ExtractIntentRequest,
    ExtractIntentResponse,
    GenerateCityPackRequest,
    GenerateCityPackResponse,
)


class AIServiceUnavailableError(Exception):
    pass


def extract_trip_intent_from_ai(
    query: str,
    supported_cities: List[str],
    allowed_preference_tags: List[str],
    allowed_traveler_types: List[str],
) -> ExtractIntentResponse:
    payload = ExtractIntentRequest(
        query=query,
        supported_cities=supported_cities,
        allowed_preference_tags=allowed_preference_tags,
        allowed_traveler_types=allowed_traveler_types,
    )

    response = _post_to_ai_service("/ai/extract-intent", payload.model_dump())

    return ExtractIntentResponse.model_validate(response.json())


def generate_city_pack_from_ai(
    city_name: str,
    user_query: str,
    traveler_type: str | None,
    preferences: list[str],
    budget_total: float | None,
) -> GenerateCityPackResponse:
    payload = GenerateCityPackRequest(
        city_name=city_name,
        user_query=user_query,
        traveler_type=traveler_type,
        preferences=preferences,
        budget_total=budget_total,
    )
    response = _post_to_ai_service("/ai/generate-city-pack", payload.model_dump())
    return GenerateCityPackResponse.model_validate(response.json())


def _post_to_ai_service(path: str, json_payload: dict):
    try:
        with httpx.Client(timeout=settings.ai_service_timeout_seconds) as client:
            response = client.post(
                f"{settings.ai_service_base_url}{path}",
                json=json_payload,
            )
            response.raise_for_status()
            return response
    except httpx.HTTPError as exc:
        raise AIServiceUnavailableError(str(exc)) from exc
