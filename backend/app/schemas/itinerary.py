from typing import List, Optional
from sqlmodel import Field, SQLModel


class ItineraryItemRead(SQLModel):
    id: int
    trip_id: int
    day_number: int
    item_order: int
    item_type: str
    title: str
    description: Optional[str] = None
    place_id: Optional[int] = None
    activity_id: Optional[int] = None
    hotel_id: Optional[int] = None


class ItineraryDay(SQLModel):
    day_number: int
    items: List[ItineraryItemRead]


class ItineraryResponse(SQLModel):
    trip_id: int
    days: List[ItineraryDay]


class ItineraryOperationPayload(SQLModel):
    item_id: Optional[int] = None
    day_number: Optional[int] = None
    target_day_number: Optional[int] = None
    target_item_order: Optional[int] = None
    ordered_item_ids: List[int] = Field(default_factory=list)
    item_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class ItineraryOperationRequest(SQLModel):
    type: str
    operation_id: str
    trip_id: int
    user_id: str
    base_version: int
    payload: ItineraryOperationPayload = Field(default_factory=ItineraryOperationPayload)


class ItineraryOperationResult(SQLModel):
    type: str
    operation_id: str
    trip_id: int
    user_id: str
    base_version: int
    current_version: int
    status: str
    payload: dict = Field(default_factory=dict)


class ConflictResponse(SQLModel):
    type: str = "ITINERARY_REJECTED"
    operation_id: str
    trip_id: int
    status: str = "rejected"
    current_version: int
    detail: str
    payload: dict = Field(default_factory=dict)


class TripVersionRead(SQLModel):
    trip_id: int
    version: int
    locked_by: Optional[str] = None
    locked_day_number: Optional[int] = None
