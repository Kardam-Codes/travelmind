from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class BookingRequestCreate(SQLModel):
    trip_id: int
    traveler_name: str
    traveler_email: str
    traveler_phone: Optional[str] = None
    total_travelers: int = 1
    budget_total: Optional[float] = None
    notes: Optional[str] = None


class BookingRequestUpdate(SQLModel):
    status: Optional[str] = None
    assigned_agent_id: Optional[int] = None


class BookingRequestRead(SQLModel):
    id: int
    organization_id: int
    trip_id: int
    requester_id: int
    traveler_name: str
    traveler_email: str
    traveler_phone: Optional[str] = None
    total_travelers: int
    budget_total: Optional[float] = None
    notes: Optional[str] = None
    status: str
    assigned_agent_id: Optional[int] = None
    created_at: datetime


class BookingOfferCreate(SQLModel):
    provider: str
    deeplink_url: str
    price: float
    commission_rate: float


class BookingOfferRead(SQLModel):
    id: int
    request_id: int
    provider: str
    deeplink_url: str
    price: float
    commission_rate: float
    created_at: datetime


class BookingClickRead(SQLModel):
    id: int
    offer_id: int
    user_id: Optional[int] = None
    referrer: Optional[str] = None
    created_at: datetime
