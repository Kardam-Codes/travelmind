from typing import Optional

from sqlmodel import Field, SQLModel


class MapRouteStopRead(SQLModel):
    item_id: Optional[int] = None
    day_number: int
    item_order: int
    title: str
    source_type: str
    source_id: Optional[int] = None
    latitude: float
    longitude: float


class MapRouteLegRead(SQLModel):
    start_title: str
    end_title: str
    distance_text: Optional[str] = None
    duration_text: Optional[str] = None


class MapBoundsRead(SQLModel):
    north: float
    south: float
    east: float
    west: float


class MapRouteResponse(SQLModel):
    trip_id: int
    day_number: Optional[int] = None
    stops: list[MapRouteStopRead]
    polyline: Optional[str] = None
    path: list[dict] = Field(default_factory=list)
    legs: list[MapRouteLegRead] = Field(default_factory=list)
    bounds: Optional[MapBoundsRead] = None
    provider_status: str = "unavailable"
    warning: Optional[str] = None
