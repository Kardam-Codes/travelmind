from typing import List, Optional

from sqlmodel import SQLModel


class ExtractIntentRequest(SQLModel):
    query: str
    supported_cities: List[str]
    allowed_preference_tags: List[str]
    allowed_traveler_types: List[str]


class ExtractIntentResponse(SQLModel):
    destination_city: Optional[str] = None
    unsupported_city: Optional[str] = None
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


class GeneratedCityRead(SQLModel):
    city: str
    state: str
    tier: str = "Tier 3"
    tourism_type: Optional[str] = None
    latitude: float
    longitude: float
    best_season: Optional[str] = None
    popularity_score: int = 60
    notes: Optional[str] = None


class GeneratedPlaceRead(SQLModel):
    name: str
    category: str
    tags: str
    rating: float
    price_estimate: float
    duration_hours: float
    latitude: float
    longitude: float
    popularity_score: int
    best_time: Optional[str] = None
    family_friendly: bool = True
    foreign_tourist_friendly: bool = True
    description: Optional[str] = None
    image_url: Optional[str] = None


class GeneratedHotelRead(SQLModel):
    name: str
    price_per_night: float
    hotel_type: str
    rating: float
    latitude: float
    longitude: float
    budget_category: str
    nearby_area: Optional[str] = None
    popularity_score: int
    tags: Optional[str] = None
    image_url: Optional[str] = None


class GeneratedActivityRead(SQLModel):
    name: str
    category: str
    tags: str
    price: float
    duration_hours: float
    rating: float
    latitude: float
    longitude: float
    near_place_name: Optional[str] = None
    popularity_score: int


class GenerateCityPackRequest(SQLModel):
    city_name: str
    user_query: str
    traveler_type: Optional[str] = None
    preferences: List[str] = []
    budget_total: Optional[float] = None


class GenerateCityPackResponse(SQLModel):
    city: GeneratedCityRead
    places: List[GeneratedPlaceRead]
    hotels: List[GeneratedHotelRead]
    activities: List[GeneratedActivityRead]
    provider: str = "fallback"
