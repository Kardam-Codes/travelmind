from typing import List

from app.database.models.trip import Trip


def generate_itinerary_items(trip: Trip, places: List, activities: List, hotels: List) -> List[dict]:
    items = []

    if hotels:
        items.append(
            {
                "day_number": 1,
                "item_order": 1,
                "item_type": "hotel",
                "title": f"Check in at {hotels[0].name}",
                "description": f"Stay in {hotels[0].city}",
                "hotel_id": hotels[0].id,
            }
        )

    place_index = 0
    activity_index = 0

    for day in range(1, trip.duration_days + 1):
        if place_index < len(places):
            place = places[place_index]
            items.append(
                {
                    "day_number": day,
                    "item_order": 2 if day == 1 and hotels else 1,
                    "item_type": "place",
                    "title": place.name,
                    "description": f"Visit this {place.category} in {place.city}",
                    "place_id": place.id,
                }
            )
            place_index += 1

        if activity_index < len(activities):
            activity = activities[activity_index]
            items.append(
                {
                    "day_number": day,
                    "item_order": 3 if day == 1 and hotels else 2,
                    "item_type": "activity",
                    "title": activity.name,
                    "description": f"Enjoy a {activity.category} activity",
                    "activity_id": activity.id,
                }
            )
            activity_index += 1

    return items
