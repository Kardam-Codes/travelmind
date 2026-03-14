"""
Feature: FastAPI Server
File Purpose: Main AI API service
Owner: Yug
Dependencies: FastAPI
Last Updated: Initial Setup
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from features.intent_extraction.intent_parser import IntentParser
from features.recommendation_engine.recommendation_engine import RecommendationEngine
from features.itinerary_generator.itinerary_generator import ItineraryGenerator

app = FastAPI(title="TravelMind AI Service")

# Initialize Service Classes
intentParser = IntentParser(llmClient=None)
recEngine = RecommendationEngine()
itineraryGen = ItineraryGenerator()

class TripRequest(BaseModel):
    userQuery: str

@app.post("/ai/generate-trip")
async def generate_trip(request: TripRequest):
    # Step 1: Extract Intent
    extractedIntent = intentParser.parse_user_intent(request.userQuery)
    
    # Step 2: Get Verified Recommendations
    filteredRecs = recEngine.get_filtered_recommendations(extractedIntent)
    
    if not filteredRecs["topPlaces"]:
        raise HTTPException(status_code=404, detail="No matching travel data found for this request.")

    # Step 3: Build the Daily Schedule
    finalItinerary = itineraryGen.generate_itinerary(
        filteredRecs, 
        extractedIntent["durationDays"]
    )

    return {
        "status": "Success",
        "tripDetails": {
            "destination": extractedIntent["destinationCity"],
            "budget": extractedIntent["budgetLevel"],
            "itinerary": finalItinerary
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)