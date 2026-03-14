from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Invite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, index=True)
    scope: str = Field(nullable=False, index=True)  # "org" or "trip"
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id", index=True)
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id", index=True)
    role: str = Field(nullable=False, default="member", index=True)
    inviter_id: int = Field(nullable=False, index=True, foreign_key="user.id")
    status: str = Field(nullable=False, default="pending", index=True)
    expires_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
