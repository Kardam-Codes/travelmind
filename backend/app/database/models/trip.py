from typing import Optional
from sqlmodel import Field, SQLModel


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    destination_city: str = Field(nullable=False, index=True)
    state: Optional[str] = None
    duration_days: int = Field(nullable=False)
    budget_total: Optional[float] = None
    preferences: Optional[str] = None
    traveler_type: Optional[str] = None
    status: str = Field(default="draft", nullable=False)
