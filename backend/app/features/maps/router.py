from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.maps.service import get_trip_route
from app.schemas.map import MapRouteResponse


router = APIRouter(prefix="/maps", tags=["Maps"])


@router.get("/trips/{trip_id}/route", response_model=MapRouteResponse)
async def get_trip_route_endpoint(
    trip_id: int,
    day_number: Optional[int] = None,
    session: Session = Depends(get_session),
):
    return await get_trip_route(session, trip_id, day_number=day_number)
