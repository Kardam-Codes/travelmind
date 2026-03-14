from typing import List, Optional

from sqlmodel import SQLModel


class ExtractIntentRequest(SQLModel):
    query: str
    supported_cities: List[str]
    allowed_preference_tags: List[str]
    allowed_traveler_types: List[str]


class ExtractIntentResponse(SQLModel):
    destination_city: Optional[str] = None
    duration_days: Optional[int] = None
    budget_total: Optional[float] = None
    budget_level: Optional[str] = None
    preferences: List[str] = []
    traveler_type: Optional[str] = None
    confidence: float = 0.0
    missing_fields: List[str] = []
    raw_reasoning_summary: Optional[str] = None
    normalized_query: str
    provider: str = "fallback"
