from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class CollaborationEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(nullable=False, index=True)
    user_id: str = Field(nullable=False, index=True)
    operation_id: Optional[str] = Field(default=None, index=True)
    base_version: Optional[int] = None
    event_type: str = Field(nullable=False, index=True)
    status: str = Field(default="applied", nullable=False, index=True)
    payload: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
