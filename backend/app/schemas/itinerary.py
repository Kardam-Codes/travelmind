from typing import List, Optional
from sqlmodel import SQLModel


class ItineraryItemRead(SQLModel):
    id: int
    trip_id: int
    day_number: int
    item_order: int
    item_type: str
    title: str
    description: Optional[str] = None
    place_id: Optional[int] = None
    activity_id: Optional[int] = None
    hotel_id: Optional[int] = None


class ItineraryDay(SQLModel):
    day_number: int
    items: List[ItineraryItemRead]


class ItineraryResponse(SQLModel):
    trip_id: int
    days: List[ItineraryDay]
