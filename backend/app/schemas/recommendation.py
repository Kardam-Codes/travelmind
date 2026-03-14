from typing import List, Optional
from sqlmodel import Field, SQLModel

from app.schemas.activity import ActivityRead
from app.schemas.hotel import HotelRead
from app.schemas.place import PlaceRead


class RecommendationRequest(SQLModel):
    destination_city: str
    duration_days: int
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None


class RecommendationResponse(SQLModel):
    destination_city: str
    places: List[PlaceRead] = Field(default_factory=list)
    activities: List[ActivityRead] = Field(default_factory=list)
    hotels: List[HotelRead] = Field(default_factory=list)
