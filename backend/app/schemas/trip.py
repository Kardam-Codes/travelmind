from typing import Optional
from sqlmodel import SQLModel


class TripCreate(SQLModel):
    destination_city: str
    duration_days: int
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None


class TripRead(SQLModel):
    id: int
    destination_city: str
    state: Optional[str] = None
    duration_days: int
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None
    status: str
