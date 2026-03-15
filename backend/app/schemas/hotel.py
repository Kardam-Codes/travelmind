from typing import Optional
from sqlmodel import SQLModel


class HotelRead(SQLModel):
    id: int
    name: str
    city: str
    state: str
    price_per_night: Optional[float] = None
    hotel_type: Optional[str] = None
    rating: Optional[float] = None
    latitude: float
    longitude: float
    budget_category: Optional[str] = None
    nearby_area: Optional[str] = None
    popularity_score: Optional[int] = None
    image_url: Optional[str] = None
