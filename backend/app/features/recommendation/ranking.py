from typing import List, Optional

from app.database.models.activity import Activity
from app.database.models.hotel import Hotel
from app.database.models.place import Place


def _split_preferences(preferences: Optional[str]) -> List[str]:
    if not preferences:
        return []
    return [item.strip().lower() for item in preferences.split(",") if item.strip()]


def rank_places(places: List[Place], preferences: Optional[str]) -> List[Place]:
    preference_list = _split_preferences(preferences)

    def score(place: Place) -> float:
        match_score = 0
        place_text = f"{place.category} {place.tags or ''} {place.name}".lower()
        for pref in preference_list:
            if pref in place_text:
                match_score += 10

        rating_score = place.rating or 0
        popularity_score = (place.popularity_score or 0) / 10
        return match_score + rating_score + popularity_score

    return sorted(places, key=score, reverse=True)


def rank_activities(activities: List[Activity], preferences: Optional[str]) -> List[Activity]:
    preference_list = _split_preferences(preferences)

    def score(activity: Activity) -> float:
        match_score = 0
        activity_text = f"{activity.category} {activity.tags or ''} {activity.name}".lower()
        for pref in preference_list:
            if pref in activity_text:
                match_score += 10

        rating_score = activity.rating or 0
        popularity_score = (activity.popularity_score or 0) / 10
        return match_score + rating_score + popularity_score

    return sorted(activities, key=score, reverse=True)


def rank_hotels(hotels: List[Hotel]) -> List[Hotel]:
    def score(hotel: Hotel) -> float:
        rating_score = hotel.rating or 0
        popularity_score = (hotel.popularity_score or 0) / 10
        return rating_score + popularity_score

    return sorted(hotels, key=score, reverse=True)
