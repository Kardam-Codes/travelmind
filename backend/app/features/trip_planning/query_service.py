import re

from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.trip import Trip
from app.features.ai.client import AIServiceUnavailableError, extract_trip_intent_from_ai
from app.features.itinerary.service import fetch_trip_itinerary, generate_trip_itinerary
from app.features.recommendation.service import get_recommendations
from app.features.trip_planning.service import create_trip_plan
from app.repositories.city_repository import get_all_cities
from app.repositories.itinerary_repository import get_itinerary_by_trip_id
from app.schemas.recommendation import RecommendationRequest
from app.schemas.trip import TripCreate, TripDashboardResponse, TripGenerationResponse


DEFAULT_DURATION_DAYS = 3
DEFAULT_BUDGET_TOTAL = 15000.0
ALLOWED_PREFERENCE_TAGS = [
    "heritage",
    "food",
    "beach",
    "nightlife",
    "market",
    "adventure",
    "relaxed",
    "family",
    "culture",
    "nature",
    "shopping",
]
ALLOWED_TRAVELER_TYPES = ["solo", "family", "couple", "friends"]


def create_trip_from_query(session: Session, query: str) -> TripGenerationResponse:
    city_names = [city.city for city in get_all_cities(session)]

    try:
        ai_intent = extract_trip_intent_from_ai(
            query=query,
            supported_cities=city_names,
            allowed_preference_tags=ALLOWED_PREFERENCE_TAGS,
            allowed_traveler_types=ALLOWED_TRAVELER_TYPES,
        )
        if ai_intent.missing_fields or ai_intent.confidence < 0.45:
            return TripGenerationResponse(
                status="clarification_needed",
                missing_fields=ai_intent.missing_fields,
                suggested_questions=_suggest_questions(ai_intent.missing_fields),
                normalized_query=ai_intent.normalized_query,
                ai_provider=ai_intent.provider,
            )

        trip_request = TripCreate(
            destination_city=ai_intent.destination_city or "",
            duration_days=ai_intent.duration_days or DEFAULT_DURATION_DAYS,
            budget_total=ai_intent.budget_total or DEFAULT_BUDGET_TOTAL,
            preferences=", ".join(ai_intent.preferences) if ai_intent.preferences else None,
            traveler_type=ai_intent.traveler_type,
        )
        trip = create_trip_plan(session, trip_request)
        dashboard = build_trip_dashboard(session, trip)
        return TripGenerationResponse(
            status="ready",
            trip=dashboard.trip,
            places=dashboard.places,
            activities=dashboard.activities,
            hotels=dashboard.hotels,
            itinerary=dashboard.itinerary,
            normalized_query=ai_intent.normalized_query,
            ai_provider=ai_intent.provider,
        )
    except AIServiceUnavailableError:
        trip_request = parse_trip_query_fallback(session, query)
        trip = create_trip_plan(session, trip_request)
        dashboard = build_trip_dashboard(session, trip)
        return TripGenerationResponse(
            status="ready",
            trip=dashboard.trip,
            places=dashboard.places,
            activities=dashboard.activities,
            hotels=dashboard.hotels,
            itinerary=dashboard.itinerary,
            normalized_query=query.strip(),
            ai_provider="fallback-rule-parser",
        )


def build_trip_dashboard(session: Session, trip: Trip) -> TripDashboardResponse:
    recommendation_request = RecommendationRequest(
        destination_city=trip.destination_city,
        duration_days=trip.duration_days,
        budget_total=trip.budget_total,
        preferences=trip.preferences,
        traveler_type=trip.traveler_type,
    )
    recommendations = get_recommendations(session, recommendation_request)
    itinerary = (
        fetch_trip_itinerary(session, trip.id)
        if get_itinerary_by_trip_id(session, trip.id)
        else generate_trip_itinerary(session, trip.id)
    )

    return TripDashboardResponse(
        trip=trip,
        places=recommendations.places,
        activities=recommendations.activities,
        hotels=recommendations.hotels,
        itinerary=itinerary,
    )


def parse_trip_query_fallback(session: Session, query: str) -> TripCreate:
    cleaned_query = query.strip()
    if not cleaned_query:
        raise HTTPException(status_code=400, detail="Trip query cannot be empty.")

    normalized_query = cleaned_query.lower()
    city_names = [city.city for city in get_all_cities(session)]
    destination_city = next((city for city in city_names if city.lower() in normalized_query), None)
    if not destination_city:
        raise HTTPException(status_code=404, detail="No supported destination found in the query.")

    duration_match = re.search(r"(\d+)\s*(day|days|night|nights)", normalized_query)
    budget_match = re.search(r"(?:under|below|budget|within)\s*(?:rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)\s*([kK]?)", normalized_query)
    traveler_type = _extract_traveler_type(normalized_query)
    preferences = _extract_preferences(normalized_query, destination_city)

    budget_total = DEFAULT_BUDGET_TOTAL
    if budget_match:
        budget_total = float(budget_match.group(1).replace(",", ""))
        if budget_match.group(2):
            budget_total *= 1000

    duration_days = int(duration_match.group(1)) if duration_match else DEFAULT_DURATION_DAYS

    return TripCreate(
        destination_city=destination_city,
        duration_days=duration_days,
        budget_total=budget_total,
        preferences=", ".join(preferences) if preferences else None,
        traveler_type=traveler_type,
    )


def _extract_preferences(query: str, city: str) -> list[str]:
    tokens = []
    if "heritage" in query or "fort" in query or "palace" in query:
        tokens.append("heritage")
    if "food" in query or "street food" in query or "cafe" in query:
        tokens.append("food")
    if "beach" in query:
        tokens.append("beach")
    if "nightlife" in query:
        tokens.append("nightlife")
    if "market" in query or "shopping" in query:
        tokens.append("market")
    if "adventure" in query or "water sport" in query or "trek" in query:
        tokens.append("adventure")
    if "relax" in query or "calm" in query or "quiet" in query:
        tokens.append("relaxed")
    if not tokens:
        tokens.append(city.lower())
    return tokens


def _extract_traveler_type(query: str) -> str | None:
    if "family" in query:
        return "family"
    if "friends" in query or "group" in query:
        return "friends"
    if "couple" in query or "honeymoon" in query:
        return "couple"
    if "solo" in query:
        return "solo"
    return None


def _suggest_questions(missing_fields: list[str]) -> list[str]:
    question_map = {
        "destination_city": "Which supported city do you want to visit?",
        "duration_days": "How many days should the trip last?",
        "budget_total": "What total budget should I plan within?",
        "traveler_type": "Who is traveling: solo, couple, family, or friends?",
    }
    return [question_map[field] for field in missing_fields if field in question_map]
