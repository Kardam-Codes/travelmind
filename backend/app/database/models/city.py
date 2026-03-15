from typing import Optional
from sqlmodel import Field, SQLModel


class City(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(index=True, nullable=False, unique=True)
    state: str = Field(nullable=False)
    tier: Optional[str] = None
    tourism_type: Optional[str] = None
    latitude: float
    longitude: float
    best_season: Optional[str] = None
    popularity_score: Optional[int] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    source: str = Field(default="seed", nullable=False)
    verified: bool = Field(default=True, nullable=False)
