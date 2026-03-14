from typing import Optional
from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    city: str = Field(nullable=False, index=True)
    state: str = Field(nullable=False)
    category: str = Field(nullable=False, index=True)
    tags: Optional[str] = None
    price: Optional[float] = None
    duration_hours: Optional[float] = None
    rating: Optional[float] = None
    latitude: float
    longitude: float
    linked_place_id: Optional[int] = Field(default=None, index=True)
    near_place_name: Optional[str] = None
    popularity_score: Optional[int] = None
