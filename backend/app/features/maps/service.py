from fastapi import HTTPException
from sqlmodel import Session

from app.features.itinerary.service import fetch_trip_itinerary
from app.features.maps.client import get_route
from app.repositories.activity_repository import get_activity_by_id, get_activities_by_city
from app.repositories.hotel_repository import get_hotel_by_id, get_hotels_by_city
from app.repositories.place_repository import get_place_by_id, get_places_by_city
from app.repositories.trip_repository import get_trip_by_id
from app.schemas.map import MapBoundsRead, MapRouteLegRead, MapRouteResponse, MapRouteStopRead


async def get_trip_route(session: Session, trip_id: int, day_number: int | None = None) -> MapRouteResponse:
    trip = get_trip_by_id(session, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    itinerary = fetch_trip_itinerary(session, trip_id)
    ordered_items = [
        item
        for day in itinerary.days
        if day_number is None or day.day_number == day_number
        for item in sorted(day.items, key=lambda value: value.item_order)
    ]

    stops = _resolve_route_stops(session, trip.destination_city, ordered_items)
    if not stops:
        return MapRouteResponse(
            trip_id=trip_id,
            day_number=day_number,
            stops=[],
            provider_status="no_stops",
            warning="No itinerary stops with coordinates were available for the map route.",
        )

    bounds = _compute_bounds(stops)
    route_response = MapRouteResponse(
        trip_id=trip_id,
        day_number=day_number,
        stops=stops,
        bounds=bounds,
        provider_status="stops_only",
        path=[{"lat": stop.latitude, "lng": stop.longitude} for stop in stops],
    )

    if len(stops) < 2:
        route_response.warning = "At least two stops are needed to draw a route."
        return route_response

    try:
        directions = await _fetch_directions_for_stops(stops)
        route_response.legs = _extract_legs(directions, stops)
        route_response.path = _extract_overview_path(directions) or route_response.path
        route_response.bounds = _extract_bounds(directions) or bounds
        route_response.provider_status = "ok"
        if not route_response.path:
            route_response.warning = "Routing provider returned no geometry. Showing markers only."
            route_response.provider_status = "partial"
    except Exception:
        route_response.provider_status = "directions_unavailable"
        route_response.warning = "Directions could not be loaded from the routing service. Showing markers only."

    return route_response


async def _fetch_directions_for_stops(stops: list[MapRouteStopRead]):
    return await get_route([(stop.latitude, stop.longitude) for stop in stops])


def _resolve_route_stops(session: Session, city_name: str, itinerary_items: list) -> list[MapRouteStopRead]:
    city_places = get_places_by_city(session, city_name)
    city_hotels = get_hotels_by_city(session, city_name)
    city_activities = get_activities_by_city(session, city_name)
    stops = []

    for item in itinerary_items:
        resolved = None
        if item.place_id:
            place = get_place_by_id(session, item.place_id)
            if place:
                resolved = MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="place",
                    source_id=place.id,
                    latitude=place.latitude,
                    longitude=place.longitude,
                )
        elif item.activity_id:
            activity = get_activity_by_id(session, item.activity_id)
            if activity:
                resolved = MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="activity",
                    source_id=activity.id,
                    latitude=activity.latitude,
                    longitude=activity.longitude,
                )
        elif item.hotel_id:
            hotel = get_hotel_by_id(session, item.hotel_id)
            if hotel:
                resolved = MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="hotel",
                    source_id=hotel.id,
                    latitude=hotel.latitude,
                    longitude=hotel.longitude,
                )
        else:
            resolved = _match_item_by_title(item, city_places, city_hotels, city_activities)

        if resolved:
            stops.append(resolved)

    return stops


def _match_item_by_title(item, city_places, city_hotels, city_activities):
    normalized_title = item.title.strip().lower()
    candidates = []

    for place in city_places:
        if place.name.strip().lower() == normalized_title:
            candidates.append(
                MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="place",
                    source_id=place.id,
                    latitude=place.latitude,
                    longitude=place.longitude,
                )
            )
    for hotel in city_hotels:
        if hotel.name.strip().lower() == normalized_title:
            candidates.append(
                MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="hotel",
                    source_id=hotel.id,
                    latitude=hotel.latitude,
                    longitude=hotel.longitude,
                )
            )
    for activity in city_activities:
        if activity.name.strip().lower() == normalized_title:
            candidates.append(
                MapRouteStopRead(
                    item_id=item.id,
                    day_number=item.day_number,
                    item_order=item.item_order,
                    title=item.title,
                    source_type="activity",
                    source_id=activity.id,
                    latitude=activity.latitude,
                    longitude=activity.longitude,
                )
            )

    return candidates[0] if len(candidates) == 1 else None


def _compute_bounds(stops: list[MapRouteStopRead]) -> MapBoundsRead:
    latitudes = [stop.latitude for stop in stops]
    longitudes = [stop.longitude for stop in stops]
    return MapBoundsRead(
        north=max(latitudes),
        south=min(latitudes),
        east=max(longitudes),
        west=min(longitudes),
    )


def _extract_legs(directions_payload: dict, stops: list[MapRouteStopRead]) -> list[MapRouteLegRead]:
    routes = directions_payload.get("routes", [])
    if not routes:
        return []
    legs = routes[0].get("legs", [])
    return [
        MapRouteLegRead(
            start_title=stops[index].title if index < len(stops) else "Stop",
            end_title=stops[index + 1].title if index + 1 < len(stops) else "Stop",
            distance_text=_format_distance(leg.get("distance")),
            duration_text=_format_duration(leg.get("duration")),
        )
        for index, leg in enumerate(legs)
    ]


def _extract_bounds(directions_payload: dict) -> MapBoundsRead | None:
    routes = directions_payload.get("routes", [])
    if not routes:
        return None
    geometry = routes[0].get("geometry", {}).get("coordinates", [])
    if not geometry:
        return None
    latitudes = [coordinate[1] for coordinate in geometry]
    longitudes = [coordinate[0] for coordinate in geometry]
    return MapBoundsRead(
        north=max(latitudes),
        south=min(latitudes),
        east=max(longitudes),
        west=min(longitudes),
    )


def _extract_overview_path(directions_payload: dict) -> list[dict]:
    routes = directions_payload.get("routes", [])
    if not routes:
        return []
    geometry = routes[0].get("geometry", {}).get("coordinates", [])
    return [{"lat": coordinate[1], "lng": coordinate[0]} for coordinate in geometry]


def _format_distance(distance_meters: float | None) -> str | None:
    if distance_meters is None:
        return None
    if distance_meters >= 1000:
        return f"{distance_meters / 1000:.1f} km"
    return f"{int(distance_meters)} m"


def _format_duration(duration_seconds: float | None) -> str | None:
    if duration_seconds is None:
        return None
    minutes = round(duration_seconds / 60)
    if minutes >= 60:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m" if remaining_minutes else f"{hours}h"
    return f"{minutes} min"
