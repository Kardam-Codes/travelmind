from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TripMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(nullable=False, index=True, foreign_key="trip.id")
    user_id: int = Field(nullable=False, index=True, foreign_key="user.id")
    role: str = Field(nullable=False, default="viewer", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
