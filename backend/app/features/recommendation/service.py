from sqlmodel import Session

from app.features.recommendation.clustering import limit_places_by_duration
from app.features.recommendation.filters import (
    filter_activities_by_preferences,
    filter_hotels_by_budget,
    filter_places_by_preferences,
)
from app.features.recommendation.ranking import rank_activities, rank_hotels, rank_places
from app.features.trip_planning.normalizer import normalize_trip_request
from app.features.trip_planning.validator import validate_trip_request
from app.repositories.activity_repository import get_activities_by_city
from app.repositories.hotel_repository import get_hotels_by_city
from app.repositories.place_repository import get_places_by_city
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse


def get_recommendations(
    session: Session,
    request_data: RecommendationRequest,
) -> RecommendationResponse:
    normalized_trip = normalize_trip_request(request_data)
    validate_trip_request(session, normalized_trip)

    places = get_places_by_city(session, normalized_trip.destination_city)
    activities = get_activities_by_city(session, normalized_trip.destination_city)
    hotels = get_hotels_by_city(session, normalized_trip.destination_city)

    places = filter_places_by_preferences(places, normalized_trip.preferences)
    activities = filter_activities_by_preferences(activities, normalized_trip.preferences)
    hotels = filter_hotels_by_budget(hotels, normalized_trip.budget_total)

    places = rank_places(places, normalized_trip.preferences)
    activities = rank_activities(activities, normalized_trip.preferences)
    hotels = rank_hotels(hotels)

    places = limit_places_by_duration(places, normalized_trip.duration_days)
    activities = activities[:8]
    hotels = hotels[:5]

    return RecommendationResponse(
        destination_city=normalized_trip.destination_city,
        places=places,
        activities=activities,
        hotels=hotels,
    )
