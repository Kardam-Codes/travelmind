import json
import os
import re
from hashlib import sha256

from pydantic import BaseModel, Field, ValidationError

from providers.heuristic_provider import HeuristicProvider
from providers.local_provider import LocalLLMProvider


class GeneratedCity(BaseModel):
    city: str
    state: str
    tier: str = "Tier 3"
    tourism_type: str | None = None
    latitude: float
    longitude: float
    best_season: str | None = None
    popularity_score: int = 60
    notes: str | None = None


class GeneratedPlace(BaseModel):
    name: str
    category: str
    tags: str
    rating: float
    price_estimate: float
    duration_hours: float
    latitude: float
    longitude: float
    popularity_score: int
    best_time: str | None = None
    family_friendly: bool = True
    foreign_tourist_friendly: bool = True
    description: str | None = None
    image_url: str | None = None


class GeneratedHotel(BaseModel):
    name: str
    price_per_night: float
    hotel_type: str
    rating: float
    latitude: float
    longitude: float
    budget_category: str
    nearby_area: str | None = None
    popularity_score: int
    tags: str | None = None
    image_url: str | None = None


class GeneratedActivity(BaseModel):
    name: str
    category: str
    tags: str
    price: float
    duration_hours: float
    rating: float
    latitude: float
    longitude: float
    near_place_name: str | None = None
    popularity_score: int


class GenerateCityPackResponse(BaseModel):
    city: GeneratedCity
    places: list[GeneratedPlace] = Field(default_factory=list)
    hotels: list[GeneratedHotel] = Field(default_factory=list)
    activities: list[GeneratedActivity] = Field(default_factory=list)
    provider: str = "heuristic-fallback"


class CityPackGenerator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompt_path = os.path.join(current_dir, "..", "..", "prompts", "city_pack_prompt.txt")
        self.local_provider = LocalLLMProvider()
        self.fallback_provider = HeuristicProvider()
        self.enable_local_generation = os.getenv("ENABLE_LOCAL_CITY_PACK_GENERATION", "false").strip().lower() in {"1", "true", "yes"}

    def generate(
        self,
        city_name: str,
        user_query: str,
        traveler_type: str | None,
        preferences: list[str],
        budget_total: float | None,
    ) -> GenerateCityPackResponse:
        with open(self.prompt_path, "r", encoding="utf-8") as file:
            template = file.read()

        formatted_prompt = (
            template.replace("{CityName}", city_name)
            .replace("{UserQuery}", user_query)
            .replace("{TravelerType}", traveler_type or "")
            .replace("{Preferences}", ", ".join(preferences))
            .replace("{BudgetTotal}", "" if budget_total is None else str(budget_total))
        )

        if not self.enable_local_generation:
            return _build_heuristic_city_pack(city_name, user_query, traveler_type, preferences, budget_total)

        for provider in (self.local_provider, self.fallback_provider):
            try:
                if provider.provider_name == "heuristic-fallback":
                    return _build_heuristic_city_pack(city_name, user_query, traveler_type, preferences, budget_total)
                raw_response = provider.generate_json(formatted_prompt)
                parsed = GenerateCityPackResponse.model_validate(
                    _coerce_city_pack_payload(json.loads(raw_response), city_name, user_query, traveler_type, preferences, budget_total)
                )
                parsed.provider = provider.provider_name
                return _normalize_city_pack(parsed, city_name)
            except (RuntimeError, TimeoutError, OSError, json.JSONDecodeError, ValidationError):
                continue

        return _build_heuristic_city_pack(city_name, user_query, traveler_type, preferences, budget_total)


def _normalize_city_pack(city_pack: GenerateCityPackResponse, city_name: str) -> GenerateCityPackResponse:
    city_pack.city.city = city_name.title()
    if len(city_pack.places) < 3 or len(city_pack.hotels) < 2 or len(city_pack.activities) < 3:
        return _build_heuristic_city_pack(
            city_name=city_name,
            user_query=city_pack.city.notes or city_name,
            traveler_type=None,
            preferences=[],
            budget_total=None,
        )
    return city_pack


def _coerce_city_pack_payload(
    payload: dict,
    city_name: str,
    user_query: str,
    traveler_type: str | None,
    preferences: list[str],
    budget_total: float | None,
) -> dict:
    if not isinstance(payload, dict):
        raise RuntimeError("Local city pack payload is not a JSON object.")

    if _looks_like_simplified_city_pack(payload):
        heuristic = _build_heuristic_city_pack(city_name, user_query, traveler_type, preferences, budget_total)
        if isinstance(payload.get("city"), str):
            heuristic.city.city = payload["city"].title()

        places = payload.get("places", [])
        for index, value in enumerate(places[: len(heuristic.places)]):
            if isinstance(value, str):
                heuristic.places[index].name = value.strip()

        hotels = payload.get("hotels", [])
        for index, value in enumerate(hotels[: len(heuristic.hotels)]):
            if isinstance(value, str):
                heuristic.hotels[index].name = value.strip()

        activities = payload.get("activities", [])
        for index, value in enumerate(activities[: len(heuristic.activities)]):
            if isinstance(value, str):
                heuristic.activities[index].name = value.strip()

        return heuristic.model_dump()

    return payload


def _looks_like_simplified_city_pack(payload: dict) -> bool:
    return (
        isinstance(payload.get("city"), str)
        and isinstance(payload.get("places"), list)
        and all(isinstance(item, str) for item in payload.get("places", []))
        and isinstance(payload.get("hotels"), list)
        and all(isinstance(item, str) for item in payload.get("hotels", []))
        and isinstance(payload.get("activities"), list)
        and all(isinstance(item, str) for item in payload.get("activities", []))
    )


def _build_heuristic_city_pack(
    city_name: str,
    user_query: str,
    traveler_type: str | None,
    preferences: list[str],
    budget_total: float | None,
) -> GenerateCityPackResponse:
    city = city_name.title()
    normalized_query = user_query.lower()
    state = _infer_state(normalized_query)
    base_lat, base_lng = _coordinates_for_city(city)
    themes = preferences or _themes_from_query(normalized_query)
    tourism_type = " ".join(themes[:3]) if themes else "culture leisure local"
    best_season = "winter"
    popularity = 68 if budget_total and budget_total > 50000 else 60

    places = []
    place_templates = [
        ("Heritage Quarter", "heritage", "heritage,architecture,walks"),
        ("Central Market", "market", "market,food,shopping"),
        ("City Lakefront", "lake", "lake,walks,relaxed"),
        ("Museum of Local Culture", "museum", "museum,culture,history"),
        ("Riverside Promenade", "viewpoint", "viewpoint,evening,walks"),
    ]
    for index, (suffix, category, tags) in enumerate(place_templates, start=1):
        lat, lng = _offset(base_lat, base_lng, index)
        places.append(
            GeneratedPlace(
                name=f"{city} {suffix}",
                category=category,
                tags=tags,
                rating=round(4.1 + (index * 0.12), 1),
                price_estimate=0 if index < 3 else 150 + (index * 120),
                duration_hours=1.5 + (index % 3) * 0.5,
                latitude=lat,
                longitude=lng,
                popularity_score=popularity + (6 - index) * 3,
                best_time=best_season,
                description=f"Generated attraction in {city} suitable for {', '.join(themes) or 'general sightseeing'}.",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/640px-No-Image-Placeholder.svg.png",
            )
        )

    hotels = []
    hotel_templates = [
        ("Central Stay", "budget", "low", 2200),
        ("Heritage Inn", "standard", "moderate", 4200),
        ("Grand Hotel", "premium", "high", 6900),
    ]
    for index, (suffix, hotel_type, budget_category, base_price) in enumerate(hotel_templates, start=1):
        lat, lng = _offset(base_lat, base_lng, index + 5)
        hotels.append(
            GeneratedHotel(
                name=f"{city} {suffix}",
                price_per_night=float(base_price),
                hotel_type=hotel_type,
                rating=round(4.0 + index * 0.2, 1),
                latitude=lat,
                longitude=lng,
                budget_category=budget_category,
                nearby_area=places[index - 1].name,
                popularity_score=72 + index * 6,
                tags="wifi, ac, breakfast, parking",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/640px-No-Image-Placeholder.svg.png",
            )
        )

    activities = []
    activity_templates = [
        ("Food Walk", "food", "food,street,local", 900, 2.0),
        ("Guided City Tour", "sightseeing", "culture,city-tour,local", 1200, 3.0),
        ("Evening Market Stroll", "shopping", "market,shopping,evening", 0, 1.5),
        ("Cultural Performance", "culture", "culture,music,evening", 1500, 2.5),
    ]
    for index, (suffix, category, tags, price, duration) in enumerate(activity_templates, start=1):
        lat, lng = _offset(base_lat, base_lng, index + 9)
        near_place = places[(index - 1) % len(places)].name
        activities.append(
            GeneratedActivity(
                name=f"{city} {suffix}",
                category=category,
                tags=tags,
                price=float(price),
                duration_hours=duration,
                rating=round(4.0 + index * 0.15, 1),
                latitude=lat,
                longitude=lng,
                near_place_name=near_place,
                popularity_score=70 + index * 5,
            )
        )

    return GenerateCityPackResponse(
        city=GeneratedCity(
            city=city,
            state=state,
            tier="Tier 3",
            tourism_type=tourism_type,
            latitude=base_lat,
            longitude=base_lng,
            best_season=best_season,
            popularity_score=popularity,
            notes=f"Generated city pack for {city} based on user query and fallback heuristics.",
        ),
        places=places,
        hotels=hotels,
        activities=activities,
        provider="heuristic-generated-city-pack",
    )


def _coordinates_for_city(city_name: str) -> tuple[float, float]:
    digest = sha256(city_name.lower().encode("utf-8")).hexdigest()
    lat_seed = int(digest[:8], 16)
    lng_seed = int(digest[8:16], 16)
    latitude = 8.0 + (lat_seed % 2600) / 100
    longitude = 68.0 + (lng_seed % 2900) / 100
    return round(latitude, 4), round(longitude, 4)


def _offset(latitude: float, longitude: float, index: int) -> tuple[float, float]:
    delta = 0.012 * index
    return round(latitude + delta, 4), round(longitude + delta / 2, 4)


def _themes_from_query(query: str) -> list[str]:
    matches = []
    for tag in ("heritage", "food", "beach", "nightlife", "market", "culture", "nature", "adventure", "relaxed", "family"):
        if tag in query:
            matches.append(tag)
    return matches or ["culture", "food", "relaxed"]


def _infer_state(query: str) -> str:
    known_states = [
        "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", "haryana",
        "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur",
        "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
        "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal",
    ]
    for state in known_states:
        if state in query:
            return state.title()
    match = re.search(r"\bin\s+([A-Za-z][A-Za-z\s]+)", query)
    if match:
        return match.group(1).strip().title()
    return "Generated Region"
