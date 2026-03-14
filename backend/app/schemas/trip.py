from typing import List, Optional
from sqlmodel import SQLModel

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


class TripQueryRequest(SQLModel):
    query: str


class TripDashboardResponse(SQLModel):
    trip: TripRead
    places: List[PlaceRead]
    activities: List[ActivityRead]
    hotels: List[HotelRead]
    itinerary: ItineraryResponse
