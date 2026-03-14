from typing import Optional
from sqlmodel import Field, SQLModel


class ItineraryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(nullable=False, index=True)
    day_number: int = Field(nullable=False, index=True)
    item_order: int = Field(default=1, nullable=False)
    item_type: str = Field(nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    place_id: Optional[int] = Field(default=None, index=True)
    activity_id: Optional[int] = Field(default=None, index=True)
    hotel_id: Optional[int] = Field(default=None, index=True)
