from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.itinerary.service import fetch_trip_itinerary, generate_trip_itinerary
from app.core.security import get_current_org_id, get_current_user_id
from app.features.trips.permissions import ensure_org_member, ensure_trip_member_role
from app.schemas.itinerary import ItineraryResponse


router = APIRouter(prefix="/itineraries", tags=["Itinerary"])


@router.post("/{trip_id}", response_model=ItineraryResponse)
def generate_itinerary_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="editor")
    return generate_trip_itinerary(session, trip_id)


@router.get("/{trip_id}", response_model=ItineraryResponse)
def get_itinerary_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    return fetch_trip_itinerary(session, trip_id)
