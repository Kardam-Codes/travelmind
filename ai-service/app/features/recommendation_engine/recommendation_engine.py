"""
Feature: Recommendation Engine
File Purpose: Filter travel catalog data
Owner: Yug
Dependencies: Python
Last Updated: Initial Setup
"""
import os
import pandas as pd

class RecommendationEngine:
    def __init__(self):
        # 1. Get the directory where this script is located
        currentDir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Navigate up to the root 'travelmind' folder, then into 'datasets'
        # The structure is: features/recommendation_engine -> features -> app -> ai-service -> travelmind
        # We need to go up 4 levels to reach travelmind/
        basePath = os.path.join(currentDir, "..", "..", "..", "..", "datasets")
        
        # 3. Load datasets using the absolute path
        self.placesData = pd.read_csv(os.path.join(basePath, "places.csv"))
        self.hotelsData = pd.read_csv(os.path.join(basePath, "hotels.csv"))
        self.activitiesData = pd.read_csv(os.path.join(basePath, "activities.csv"))

    def get_filtered_recommendations(self, intentData: dict):
        targetCity = intentData.get("destinationCity")
        budget = intentData.get("budgetLevel")
        interests = [i.lower() for i in intentData.get("travelInterests", [])]

        # 1. Filter Hotels by City and Budget
        matchedHotels = self.hotelsData[
            (self.hotelsData['city'].str.lower() == targetCity.lower()) & 
            (self.hotelsData['budget_category'] == budget)
        ].sort_values(by="popularity_score", ascending=False)

        # 2. Filter Places by interest tags
        matchedPlaces = self.placesData[
            (self.placesData['city'].str.lower() == targetCity.lower()) &
            (self.placesData['tags'].apply(lambda x: any(interest in str(x).lower() for interest in interests)))
        ].sort_values(by="popularity_score", ascending=False)

        # 3. Filter Activities
        matchedActivities = self.activitiesData[
            (self.activitiesData['city'].str.lower() == targetCity.lower())
        ].sort_values(by="popularity_score", ascending=False)

        return {
            "topHotels": matchedHotels.head(3).to_dict(orient="records"),
            "topPlaces": matchedPlaces.head(10).to_dict(orient="records"),
            "topActivities": matchedActivities.head(5).to_dict(orient="records")
        }