from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BookingRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(nullable=False, index=True, foreign_key="organization.id")
    trip_id: int = Field(nullable=False, index=True, foreign_key="trip.id")
    requester_id: int = Field(nullable=False, index=True, foreign_key="user.id")
    traveler_name: str = Field(nullable=False)
    traveler_email: str = Field(nullable=False)
    traveler_phone: Optional[str] = None
    total_travelers: int = Field(default=1, nullable=False)
    budget_total: Optional[float] = None
    notes: Optional[str] = None
    status: str = Field(default="pending", nullable=False, index=True)
    assigned_agent_id: Optional[int] = Field(default=None, index=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


class BookingOffer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(nullable=False, index=True, foreign_key="bookingrequest.id")
    provider: str = Field(nullable=False, index=True)
    deeplink_url: str = Field(nullable=False)
    price: float = Field(nullable=False)
    commission_rate: float = Field(default=0.0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


class BookingClick(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    offer_id: int = Field(nullable=False, index=True, foreign_key="bookingoffer.id")
    user_id: Optional[int] = Field(default=None, index=True, foreign_key="user.id")
    referrer: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
