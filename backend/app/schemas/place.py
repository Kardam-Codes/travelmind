from typing import Optional
from sqlmodel import SQLModel


class PlaceRead(SQLModel):
    id: int
    name: str
    city: str
    state: str
    category: str
    tags: Optional[str] = None
    rating: Optional[float] = None
    price_estimate: Optional[float] = None
    duration_hours: Optional[float] = None
    latitude: float
    longitude: float
    popularity_score: Optional[int] = None
    best_time: Optional[str] = None
    family_friendly: bool = False
    foreign_tourist_friendly: bool = False
