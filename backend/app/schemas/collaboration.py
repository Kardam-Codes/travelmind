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
    operation_id: Optional[str] = None
    base_version: Optional[int] = None
    event_type: str
    status: str
    payload: Optional[str] = None
    created_at: str


class WebSocketMessage(SQLModel):
    type: str
    trip_id: int
    user_id: Optional[str] = None
    payload: Optional[dict] = None


class PresenceMessage(SQLModel):
    type: str = "USER_PRESENCE"
    trip_id: int
    active_users: list[str]
