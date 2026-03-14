from sqlmodel import Session

from app.database.models.trip import Trip
from app.features.trip_planning.normalizer import normalize_trip_request
from app.features.trip_planning.validator import validate_trip_request
from app.repositories.trip_repository import create_trip, get_all_trips, get_trip_by_id
from app.repositories.trip_member_repository import create_trip_member
from app.database.models.trip_member import TripMember
from app.schemas.trip import TripCreate


def create_trip_plan(session: Session, trip_data: TripCreate, organization_id: int, user_id: int) -> Trip:
    normalized_trip = normalize_trip_request(trip_data)
    city = validate_trip_request(session, normalized_trip)

    trip = Trip(
        organization_id=organization_id,
        created_by=user_id,
        destination_city=normalized_trip.destination_city,
        state=city.state,
        duration_days=normalized_trip.duration_days,
        budget_total=normalized_trip.budget_total,
        preferences=normalized_trip.preferences,
        traveler_type=normalized_trip.traveler_type,
        status="draft",
    )

    created_trip = create_trip(session, trip)
    create_trip_member(
        session,
        TripMember(trip_id=created_trip.id, user_id=user_id, role="owner"),
    )
    return created_trip


def fetch_trip(session: Session, trip_id: int):
    return get_trip_by_id(session, trip_id)


def fetch_all_trips(session: Session, organization_id: int):
    return get_all_trips(session, organization_id)
