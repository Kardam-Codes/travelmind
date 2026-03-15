from typing import Optional
from sqlmodel import Field, SQLModel


class Hotel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    city: str = Field(nullable=False, index=True)
    state: str = Field(nullable=False)
    price_per_night: Optional[float] = None
    hotel_type: Optional[str] = Field(default=None, index=True)
    rating: Optional[float] = None
    latitude: float
    longitude: float
    budget_category: Optional[str] = Field(default=None, index=True)
    nearby_area: Optional[str] = None
    popularity_score: Optional[int] = None
    image_url: Optional[str] = None
    source: str = Field(default="seed", nullable=False)
    verified: bool = Field(default=True, nullable=False)
