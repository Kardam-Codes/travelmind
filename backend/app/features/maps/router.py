from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.core.security import get_current_org_id, get_current_user_id
from app.features.trips.permissions import ensure_org_member, ensure_trip_member_role
from app.features.maps.service import get_trip_route
from app.schemas.map import MapRouteResponse


router = APIRouter(prefix="/maps", tags=["Maps"])


@router.get("/trips/{trip_id}/route", response_model=MapRouteResponse)
async def get_trip_route_endpoint(
    trip_id: int,
    day_number: Optional[int] = None,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    return await get_trip_route(session, trip_id, day_number=day_number)
