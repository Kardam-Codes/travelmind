from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.city_repository import get_city_by_name
from app.schemas.trip import TripCreate


def validate_trip_request(session: Session, trip_data: TripCreate):
    if trip_data.duration_days <= 0:
        raise HTTPException(status_code=400, detail="Duration must be at least 1 day.")

    if trip_data.budget_total is not None and trip_data.budget_total < 0:
        raise HTTPException(status_code=400, detail="Budget cannot be negative.")

    city = get_city_by_name(session, trip_data.destination_city)
    if not city:
        raise HTTPException(status_code=404, detail="Destination city is not supported.")

    return city
