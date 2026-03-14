from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class CommentCreate(SQLModel):
    itinerary_item_id: Optional[int] = None
    body: str


class CommentRead(SQLModel):
    id: int
    trip_id: int
    itinerary_item_id: Optional[int] = None
    author_id: int
    body: str
    created_at: datetime
