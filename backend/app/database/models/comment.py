from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(nullable=False, index=True, foreign_key="trip.id")
    itinerary_item_id: Optional[int] = Field(default=None, index=True, foreign_key="itineraryitem.id")
    author_id: int = Field(nullable=False, index=True, foreign_key="user.id")
    body: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
