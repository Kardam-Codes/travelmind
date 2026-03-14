import httpx

from app.core.config import settings


async def get_route(coordinates: list[tuple[float, float]]):
    if len(coordinates) < 2:
        raise ValueError("At least two coordinates are required to request a route.")

    coordinate_path = ";".join(f"{longitude},{latitude}" for latitude, longitude in coordinates)
    route_url = f"{settings.routing_base_url.rstrip('/')}/route/v1/driving/{coordinate_path}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(route_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
