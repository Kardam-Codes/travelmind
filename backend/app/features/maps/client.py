import httpx

from app.core.config import settings


DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


async def get_distance_matrix(origins: str, destinations: str):
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": settings.google_maps_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(DISTANCE_MATRIX_URL, params=params)
        response.raise_for_status()
        return response.json()


async def get_directions(origin: str, destination: str, waypoints: str | None = None):
    params = {
        "origin": origin,
        "destination": destination,
        "key": settings.google_maps_api_key,
    }
    if waypoints:
        params["waypoints"] = waypoints

    async with httpx.AsyncClient() as client:
        response = await client.get(DIRECTIONS_URL, params=params)
        response.raise_for_status()
        return response.json()
