"""
Feature: FastAPI Server
File Purpose: Main AI API service
Owner: Yug
Dependencies: FastAPI
Last Updated: 2026-03-14
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field

from features.city_generation.generator import CityPackGenerator, GenerateCityPackResponse
from features.intent_extraction.intent_parser import ExtractIntentResponse, IntentParser


app = FastAPI(title="TravelMind AI Service")
intent_parser = IntentParser()
city_pack_generator = CityPackGenerator()


class ExtractIntentRequest(BaseModel):
    query: str
    supported_cities: list[str] = Field(default_factory=list)
    allowed_preference_tags: list[str] = Field(default_factory=list)
    allowed_traveler_types: list[str] = Field(default_factory=list)


class GenerateCityPackRequest(BaseModel):
    city_name: str
    user_query: str
    traveler_type: str | None = None
    preferences: list[str] = Field(default_factory=list)
    budget_total: float | None = None


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ai-service"}


@app.post("/ai/extract-intent", response_model=ExtractIntentResponse)
async def extract_intent(request: ExtractIntentRequest):
    return intent_parser.parse_user_intent(
        user_query=request.query,
        supported_cities=request.supported_cities,
        allowed_preference_tags=request.allowed_preference_tags,
        allowed_traveler_types=request.allowed_traveler_types,
    )


@app.post("/ai/generate-city-pack", response_model=GenerateCityPackResponse)
async def generate_city_pack(request: GenerateCityPackRequest):
    return city_pack_generator.generate(
        city_name=request.city_name,
        user_query=request.user_query,
        traveler_type=request.traveler_type,
        preferences=request.preferences,
        budget_total=request.budget_total,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
