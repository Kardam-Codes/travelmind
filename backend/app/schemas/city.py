from typing import Optional
from sqlmodel import SQLModel


class CityRead(SQLModel):
    id: int
    city: str
    state: str
    tier: Optional[str] = None
    tourism_type: Optional[str] = None
    latitude: float
    longitude: float
    best_season: Optional[str] = None
    popularity_score: Optional[int] = None
    notes: Optional[str] = None
