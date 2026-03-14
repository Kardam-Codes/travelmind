from app.schemas.trip import TripCreate


def normalize_trip_request(trip_data: TripCreate) -> TripCreate:
    cleaned_city = trip_data.destination_city.strip().title()
    cleaned_preferences = trip_data.preferences.strip().lower() if trip_data.preferences else None
    cleaned_traveler_type = trip_data.traveler_type.strip().lower() if trip_data.traveler_type else None

    return TripCreate(
        destination_city=cleaned_city,
        duration_days=trip_data.duration_days,
        budget_total=trip_data.budget_total,
        preferences=cleaned_preferences,
        traveler_type=cleaned_traveler_type,
    )
