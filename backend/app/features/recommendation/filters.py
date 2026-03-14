from typing import List, Optional

from app.database.models.activity import Activity
from app.database.models.hotel import Hotel
from app.database.models.place import Place


def _split_preferences(preferences: Optional[str]) -> List[str]:
    if not preferences:
        return []
    return [item.strip().lower() for item in preferences.split(",") if item.strip()]


def filter_places_by_preferences(places: List[Place], preferences: Optional[str]) -> List[Place]:
    preference_list = _split_preferences(preferences)
    if not preference_list:
        return places

    filtered = []
    for place in places:
        place_text = f"{place.category} {place.tags or ''} {place.name}".lower()
        if any(pref in place_text for pref in preference_list):
            filtered.append(place)

    return filtered or places


def filter_activities_by_preferences(
    activities: List[Activity],
    preferences: Optional[str],
) -> List[Activity]:
    preference_list = _split_preferences(preferences)
    if not preference_list:
        return activities

    filtered = []
    for activity in activities:
        activity_text = f"{activity.category} {activity.tags or ''} {activity.name}".lower()
        if any(pref in activity_text for pref in preference_list):
            filtered.append(activity)

    return filtered or activities


def filter_hotels_by_budget(hotels: List[Hotel], budget_total: Optional[float]) -> List[Hotel]:
    if budget_total is None:
        return hotels

    if budget_total <= 10000:
        preferred_categories = {"low"}
    elif budget_total <= 30000:
        preferred_categories = {"low", "moderate"}
    else:
        preferred_categories = {"low", "moderate", "high", "premium"}

    filtered = [hotel for hotel in hotels if (hotel.budget_category or "").lower() in preferred_categories]
    return filtered or hotels
