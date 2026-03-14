from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.itinerary.service import fetch_trip_itinerary, generate_trip_itinerary
from app.schemas.itinerary import ItineraryResponse


router = APIRouter(prefix="/itineraries", tags=["Itinerary"])


@router.post("/{trip_id}", response_model=ItineraryResponse)
def generate_itinerary_endpoint(trip_id: int, session: Session = Depends(get_session)):
    return generate_trip_itinerary(session, trip_id)


@router.get("/{trip_id}", response_model=ItineraryResponse)
def get_itinerary_endpoint(trip_id: int, session: Session = Depends(get_session)):
    return fetch_trip_itinerary(session, trip_id)
