"""
Feature: Trip Planning Service
File Purpose: Handle trip creation workflow using normalization, validation, and persistence
Owner: Misha
Dependencies: app/database/models/trip.py, app/features/trip_planning/normalizer.py, app/features/trip_planning/validator.py, app/repositories/trip_repository.py
Last Updated: 2026-03-14
"""

from sqlmodel import Session

from app.database.models.trip import Trip
from app.features.trip_planning.normalizer import normalize_trip_request
from app.features.trip_planning.validator import validate_trip_request
from app.repositories.trip_repository import create_trip, get_all_trips, get_trip_by_id
from app.schemas.trip import TripCreate


def create_trip_plan(session: Session, trip_data: TripCreate) -> Trip:
    normalized_trip = normalize_trip_request(trip_data)
    city = validate_trip_request(session, normalized_trip)

    trip = Trip(
        destination_city=normalized_trip.destination_city,
        state=city.state,
        duration_days=normalized_trip.duration_days,
        budget_total=normalized_trip.budget_total,
        preferences=normalized_trip.preferences,
        traveler_type=normalized_trip.traveler_type,
        status="draft",
    )

    return create_trip(session, trip)


def fetch_trip(session: Session, trip_id: int):
    return get_trip_by_id(session, trip_id)


def fetch_all_trips(session: Session):
    return get_all_trips(session)
