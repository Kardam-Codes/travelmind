"""
Feature: Itinerary Generator
File Purpose: Generate day-by-day itinerary
Owner: Yug
Dependencies: Python
Last Updated: Initial Setup
"""
class ItineraryGenerator:
    def generate_itinerary(self, recommendationData: dict, duration: int):
        itineraryList = []
        places = recommendationData["topPlaces"]
        activities = recommendationData["topActivities"]
        hotel = recommendationData["topHotels"][0] if recommendationData["topHotels"] else None

        for day in range(1, duration + 1):
            # Simple logic: 2 places and 1 activity per day
            dayPlan = {
                "dayNumber": day,
                "stayAt": hotel["name"] if hotel else "Standard Accommodation",
                "schedule": {
                    "morning": places.pop(0) if places else None,
                    "afternoon": activities.pop(0) if activities else None,
                    "evening": places.pop(0) if places else None
                }
            }
            itineraryList.append(dayPlan)

        return itineraryList