from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.itinerary import ItineraryItem
from app.features.itinerary.generator import generate_itinerary_items
from app.features.itinerary.optimizer import optimize_itinerary_items
from app.features.recommendation.service import get_recommendations
from app.repositories.itinerary_repository import (
    create_itinerary_item,
    delete_itinerary_by_trip_id,
    get_itinerary_by_trip_id,
    persist_changes,
)
from app.repositories.trip_repository import get_trip_by_id, save_trip
from app.schemas.itinerary import ItineraryDay, ItineraryResponse
from app.schemas.recommendation import RecommendationRequest


def generate_trip_itinerary(session: Session, trip_id: int) -> ItineraryResponse:
    trip = get_trip_by_id(session, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    recommendation_request = RecommendationRequest(
        destination_city=trip.destination_city,
        duration_days=trip.duration_days,
        budget_total=trip.budget_total,
        preferences=trip.preferences,
        traveler_type=trip.traveler_type,
    )
    recommendations = get_recommendations(session, recommendation_request)

    raw_items = generate_itinerary_items(
        trip=trip,
        places=recommendations.places,
        activities=recommendations.activities,
        hotels=recommendations.hotels,
    )
    optimized_items = optimize_itinerary_items(raw_items)

    delete_itinerary_by_trip_id(session, trip_id)

    saved_items = []
    for item in optimized_items:
        itinerary_item = ItineraryItem(
            trip_id=trip_id,
            day_number=item["day_number"],
            item_order=item["item_order"],
            item_type=item["item_type"],
            title=item["title"],
            description=item.get("description"),
            place_id=item.get("place_id"),
            activity_id=item.get("activity_id"),
            hotel_id=item.get("hotel_id"),
        )
        saved_items.append(create_itinerary_item(session, itinerary_item))

    persist_changes(session)
    for item in saved_items:
        session.refresh(item)

    trip.version += 1
    save_trip(session, trip)

    return _build_itinerary_response(trip_id, saved_items)


def fetch_trip_itinerary(session: Session, trip_id: int) -> ItineraryResponse:
    trip = get_trip_by_id(session, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    items = get_itinerary_by_trip_id(session, trip_id)
    return _build_itinerary_response(trip_id, items)


def _build_itinerary_response(trip_id: int, items: list) -> ItineraryResponse:
    days_map = {}

    for item in items:
        days_map.setdefault(item.day_number, []).append(item)

    days = [ItineraryDay(day_number=day_number, items=day_items) for day_number, day_items in sorted(days_map.items())]
    return ItineraryResponse(trip_id=trip_id, days=days)
