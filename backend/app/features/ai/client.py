from typing import List

import httpx

from app.core.config import settings
from app.schemas.ai import ExtractIntentRequest, ExtractIntentResponse


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

    try:
        with httpx.Client(timeout=settings.ai_service_timeout_seconds) as client:
            response = client.post(
                f"{settings.ai_service_base_url}/ai/extract-intent",
                json=payload.model_dump(),
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AIServiceUnavailableError(str(exc)) from exc

    return ExtractIntentResponse.model_validate(response.json())
