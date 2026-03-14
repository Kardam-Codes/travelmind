from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class InviteCreate(SQLModel):
    email: str
    scope: str
    role: str
    organization_id: Optional[int] = None
    trip_id: Optional[int] = None
    expires_in_hours: Optional[int] = 72


class InviteRead(SQLModel):
    id: int
    token: str
    email: str
    scope: str
    role: str
    organization_id: Optional[int] = None
    trip_id: Optional[int] = None
    status: str
    expires_at: Optional[datetime] = None
    created_at: datetime


class InviteAcceptRequest(SQLModel):
    token: str
