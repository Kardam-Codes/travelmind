from typing import List
from sqlmodel import SQLModel


class BookingKPI(SQLModel):
    total_requests: int
    total_offers: int
    total_clicks: int
    total_commission: float
    conversion_rate: float


class TopDestination(SQLModel):
    destination_city: str
    count: int


class AgencyReport(SQLModel):
    kpis: BookingKPI
    top_destinations: List[TopDestination]
