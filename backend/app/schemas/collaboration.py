from typing import Optional
from sqlmodel import SQLModel


class CollaborationEventCreate(SQLModel):
    trip_id: int
    user_id: str
    event_type: str
    payload: Optional[str] = None


class CollaborationEventRead(SQLModel):
    id: int
    trip_id: int
    user_id: str
    event_type: str
    payload: Optional[str] = None


class WebSocketMessage(SQLModel):
    type: str
    trip_id: int
    user_id: Optional[str] = None
    payload: Optional[dict] = None
