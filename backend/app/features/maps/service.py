from app.features.maps.client import get_directions, get_distance_matrix


async def fetch_travel_times(origins: str, destinations: str):
    return await get_distance_matrix(origins, destinations)


async def fetch_route(origin: str, destination: str, waypoints: str | None = None):
    return await get_directions(origin, destination, waypoints)
