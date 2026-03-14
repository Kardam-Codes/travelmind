from typing import Optional
from sqlmodel import SQLModel


class ActivityRead(SQLModel):
    id: int
    name: str
    city: str
    state: str
    category: str
    tags: Optional[str] = None
    price: Optional[float] = None
    duration_hours: Optional[float] = None
    rating: Optional[float] = None
    latitude: float
    longitude: float
    linked_place_id: Optional[int] = None
    near_place_name: Optional[str] = None
    popularity_score: Optional[int] = None
