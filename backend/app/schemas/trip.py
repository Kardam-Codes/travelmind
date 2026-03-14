from typing import List, Optional
from sqlmodel import Field, SQLModel

from app.schemas.activity import ActivityRead
from app.schemas.hotel import HotelRead
from app.schemas.itinerary import ItineraryResponse
from app.schemas.place import PlaceRead


class TripCreate(SQLModel):
    destination_city: str
    duration_days: int
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None


class TripRead(SQLModel):
    id: int
    destination_city: str
    state: Optional[str] = None
    duration_days: int
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None
    status: str
    version: int
    locked_by: Optional[str] = None
    locked_day_number: Optional[int] = None


class TripQueryRequest(SQLModel):
    query: str


class TripDashboardResponse(SQLModel):
    trip: TripRead
    places: List[PlaceRead]
    activities: List[ActivityRead]
    hotels: List[HotelRead]
    itinerary: ItineraryResponse


class TripGenerationResponse(SQLModel):
    status: str = "ready"
    trip: Optional[TripRead] = None
    places: List[PlaceRead] = Field(default_factory=list)
    activities: List[ActivityRead] = Field(default_factory=list)
    hotels: List[HotelRead] = Field(default_factory=list)
    itinerary: Optional[ItineraryResponse] = None
    missing_fields: List[str] = Field(default_factory=list)
    suggested_questions: List[str] = Field(default_factory=list)
    normalized_query: Optional[str] = None
    ai_provider: Optional[str] = None
