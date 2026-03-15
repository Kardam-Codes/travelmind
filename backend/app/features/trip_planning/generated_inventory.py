from pathlib import Path
import csv

from sqlmodel import Session, select

from app.database.models.activity import Activity
from app.database.models.city import City
from app.database.models.hotel import Hotel
from app.database.models.place import Place
from app.schemas.ai import GenerateCityPackResponse


DATASET_DIR = Path(__file__).resolve().parents[4] / "datasets"


def persist_generated_city_pack(session: Session, city_pack: GenerateCityPackResponse) -> City:
    city_data = city_pack.city
    existing_city = session.exec(
        select(City).where(City.city == city_data.city).where(City.state == city_data.state)
    ).first()
    if existing_city:
        _fill_city_fields(existing_city, city_data)
        if not existing_city.source:
            existing_city.source = "ai"
        session.add(existing_city)
        session.commit()
        session.refresh(existing_city)
        city = existing_city
    else:
        city = City(
            city=city_data.city,
            state=city_data.state,
            tier=city_data.tier,
            tourism_type=city_data.tourism_type,
            latitude=city_data.latitude,
            longitude=city_data.longitude,
            best_season=city_data.best_season,
            popularity_score=city_data.popularity_score,
            notes=city_data.notes,
            source="ai",
            verified=False,
        )
        session.add(city)
        session.commit()
        session.refresh(city)

    place_name_to_id: dict[str, int] = {}
    for place_data in city_pack.places:
        existing_place = session.exec(
            select(Place)
            .where(Place.name == place_data.name)
            .where(Place.city == city.city)
            .where(Place.state == city.state)
        ).first()
        if existing_place:
            _fill_place_fields(existing_place, place_data)
            if not existing_place.source:
                existing_place.source = "ai"
            session.add(existing_place)
            session.flush()
            place_name_to_id[existing_place.name] = existing_place.id
        else:
            place = Place(
                name=place_data.name,
                city=city.city,
                state=city.state,
                category=place_data.category,
                tags=place_data.tags,
                rating=place_data.rating,
                price_estimate=place_data.price_estimate,
                duration_hours=place_data.duration_hours,
                latitude=place_data.latitude,
                longitude=place_data.longitude,
                popularity_score=place_data.popularity_score,
                best_time=place_data.best_time,
                family_friendly=place_data.family_friendly,
                foreign_tourist_friendly=place_data.foreign_tourist_friendly,
                image_url=place_data.image_url,
                source="ai",
                verified=False,
            )
            session.add(place)
            session.flush()
            place_name_to_id[place.name] = place.id

    for hotel_data in city_pack.hotels:
        existing_hotel = session.exec(
            select(Hotel)
            .where(Hotel.name == hotel_data.name)
            .where(Hotel.city == city.city)
            .where(Hotel.state == city.state)
        ).first()
        if existing_hotel:
            _fill_hotel_fields(existing_hotel, hotel_data)
            if not existing_hotel.source:
                existing_hotel.source = "ai"
            session.add(existing_hotel)
        else:
            session.add(
                Hotel(
                    name=hotel_data.name,
                    city=city.city,
                    state=city.state,
                    price_per_night=hotel_data.price_per_night,
                    hotel_type=hotel_data.hotel_type,
                    rating=hotel_data.rating,
                    latitude=hotel_data.latitude,
                    longitude=hotel_data.longitude,
                    budget_category=hotel_data.budget_category,
                    nearby_area=hotel_data.nearby_area,
                    popularity_score=hotel_data.popularity_score,
                    image_url=hotel_data.image_url,
                    source="ai",
                    verified=False,
                )
            )

    for activity_data in city_pack.activities:
        existing_activity = session.exec(
            select(Activity)
            .where(Activity.name == activity_data.name)
            .where(Activity.city == city.city)
            .where(Activity.state == city.state)
        ).first()
        if existing_activity:
            _fill_activity_fields(existing_activity, activity_data, place_name_to_id)
            if not existing_activity.source:
                existing_activity.source = "ai"
            session.add(existing_activity)
        else:
            session.add(
                Activity(
                    name=activity_data.name,
                    city=city.city,
                    state=city.state,
                    category=activity_data.category,
                    tags=activity_data.tags,
                    price=activity_data.price,
                    duration_hours=activity_data.duration_hours,
                    rating=activity_data.rating,
                    latitude=activity_data.latitude,
                    longitude=activity_data.longitude,
                    linked_place_id=place_name_to_id.get(activity_data.near_place_name or ""),
                    near_place_name=activity_data.near_place_name,
                    popularity_score=activity_data.popularity_score,
                    image_url=activity_data.image_url,
                    source="ai",
                    verified=False,
                )
            )

    session.commit()
    _append_city_pack_to_datasets(city_pack)
    return city


def _fill_city_fields(existing_city: City, city_data) -> None:
    if not existing_city.tier:
        existing_city.tier = city_data.tier
    if not existing_city.tourism_type:
        existing_city.tourism_type = city_data.tourism_type
    if not existing_city.latitude:
        existing_city.latitude = city_data.latitude
    if not existing_city.longitude:
        existing_city.longitude = city_data.longitude
    if not existing_city.best_season:
        existing_city.best_season = city_data.best_season
    if not existing_city.popularity_score:
        existing_city.popularity_score = city_data.popularity_score
    if not existing_city.notes:
        existing_city.notes = city_data.notes
    if not existing_city.image_url:
        existing_city.image_url = city_data.image_url


def _fill_place_fields(existing_place: Place, place_data) -> None:
    if not existing_place.category:
        existing_place.category = place_data.category
    if not existing_place.tags:
        existing_place.tags = place_data.tags
    if not existing_place.rating:
        existing_place.rating = place_data.rating
    if not existing_place.price_estimate:
        existing_place.price_estimate = place_data.price_estimate
    if not existing_place.duration_hours:
        existing_place.duration_hours = place_data.duration_hours
    if not existing_place.latitude:
        existing_place.latitude = place_data.latitude
    if not existing_place.longitude:
        existing_place.longitude = place_data.longitude
    if not existing_place.popularity_score:
        existing_place.popularity_score = place_data.popularity_score
    if not existing_place.best_time:
        existing_place.best_time = place_data.best_time
    if existing_place.family_friendly is None:
        existing_place.family_friendly = place_data.family_friendly
    if existing_place.foreign_tourist_friendly is None:
        existing_place.foreign_tourist_friendly = place_data.foreign_tourist_friendly
    if not existing_place.image_url:
        existing_place.image_url = place_data.image_url


def _fill_hotel_fields(existing_hotel: Hotel, hotel_data) -> None:
    if not existing_hotel.price_per_night:
        existing_hotel.price_per_night = hotel_data.price_per_night
    if not existing_hotel.hotel_type:
        existing_hotel.hotel_type = hotel_data.hotel_type
    if not existing_hotel.rating:
        existing_hotel.rating = hotel_data.rating
    if not existing_hotel.latitude:
        existing_hotel.latitude = hotel_data.latitude
    if not existing_hotel.longitude:
        existing_hotel.longitude = hotel_data.longitude
    if not existing_hotel.budget_category:
        existing_hotel.budget_category = hotel_data.budget_category
    if not existing_hotel.nearby_area:
        existing_hotel.nearby_area = hotel_data.nearby_area
    if not existing_hotel.popularity_score:
        existing_hotel.popularity_score = hotel_data.popularity_score
    if not existing_hotel.image_url:
        existing_hotel.image_url = hotel_data.image_url


def _fill_activity_fields(existing_activity: Activity, activity_data, place_name_to_id: dict[str, int]) -> None:
    if not existing_activity.category:
        existing_activity.category = activity_data.category
    if not existing_activity.tags:
        existing_activity.tags = activity_data.tags
    if not existing_activity.price:
        existing_activity.price = activity_data.price
    if not existing_activity.duration_hours:
        existing_activity.duration_hours = activity_data.duration_hours
    if not existing_activity.rating:
        existing_activity.rating = activity_data.rating
    if not existing_activity.latitude:
        existing_activity.latitude = activity_data.latitude
    if not existing_activity.longitude:
        existing_activity.longitude = activity_data.longitude
    if not existing_activity.linked_place_id:
        existing_activity.linked_place_id = place_name_to_id.get(activity_data.near_place_name or "")
    if not existing_activity.near_place_name:
        existing_activity.near_place_name = activity_data.near_place_name
    if not existing_activity.popularity_score:
        existing_activity.popularity_score = activity_data.popularity_score
    if not existing_activity.image_url:
        existing_activity.image_url = activity_data.image_url


def _append_city_pack_to_datasets(city_pack: GenerateCityPackResponse) -> None:
    city = city_pack.city
    _append_row_if_missing(
        DATASET_DIR / "city_master_list.csv",
        match_criteria={"city": city.city, "state": city.state},
        row={
            "city": city.city,
            "state": city.state,
            "tier": city.tier,
            "tourism_type": city.tourism_type or "",
            "latitude": f"{city.latitude:.4f}",
            "longitude": f"{city.longitude:.4f}",
            "best_season": city.best_season or "",
            "popularity_score": city.popularity_score,
            "notes": city.notes or "",
        },
    )

    next_place_id = _next_sequence_value(DATASET_DIR / "places.csv", "P")
    next_hotel_id = _next_sequence_value(DATASET_DIR / "hotels.csv", "H")
    next_activity_id = _next_sequence_value(DATASET_DIR / "activities.csv", "A")
    place_ids: dict[str, str] = {}

    for place_data in city_pack.places:
        external_id = f"P{next_place_id:03d}"
        next_place_id += 1
        place_ids[place_data.name] = external_id
        _append_row_if_missing(
            DATASET_DIR / "places.csv",
            match_criteria={"name": place_data.name, "city": city.city, "state": city.state},
            row={
                "id": external_id,
                "name": place_data.name,
                "city": city.city,
                "state": city.state,
                "category": place_data.category,
                "tags": place_data.tags,
                "rating": place_data.rating,
                "price_estimate": place_data.price_estimate,
                "duration_hours": place_data.duration_hours,
                "latitude": place_data.latitude,
                "longitude": place_data.longitude,
                "popularity_score": place_data.popularity_score,
                "best_time": place_data.best_time or "",
                "family_friendly": str(place_data.family_friendly).lower(),
                "foreign_tourist_friendly": str(place_data.foreign_tourist_friendly).lower(),
                "description": place_data.description or "",
                "image_url": place_data.image_url or "",
            },
        )

    for hotel_data in city_pack.hotels:
        _append_row_if_missing(
            DATASET_DIR / "hotels.csv",
            match_criteria={"name": hotel_data.name, "city": city.city, "state": city.state},
            row={
                "id": f"H{next_hotel_id:03d}",
                "name": hotel_data.name,
                "city": city.city,
                "state": city.state,
                "price_per_night": hotel_data.price_per_night,
                "hotel_type": hotel_data.hotel_type,
                "rating": hotel_data.rating,
                "latitude": hotel_data.latitude,
                "longitude": hotel_data.longitude,
                "budget_category": hotel_data.budget_category,
                "nearby_area": hotel_data.nearby_area or "",
                "popularity_score": hotel_data.popularity_score,
                "tags": hotel_data.tags or "",
                "image_url": hotel_data.image_url or "",
            },
        )
        next_hotel_id += 1

    for activity_data in city_pack.activities:
        _append_row_if_missing(
            DATASET_DIR / "activities.csv",
            match_criteria={"name": activity_data.name, "city": city.city, "state": city.state},
            row={
                "id": f"A{next_activity_id:03d}",
                "name": activity_data.name,
                "city": city.city,
                "state": city.state,
                "category": activity_data.category,
                "tags": activity_data.tags,
                "price": activity_data.price,
                "duration_hours": activity_data.duration_hours,
                "rating": activity_data.rating,
                "latitude": activity_data.latitude,
                "longitude": activity_data.longitude,
                "linked_place_id": place_ids.get(activity_data.near_place_name or "", ""),
                "near_place_name": activity_data.near_place_name or "",
                "popularity_score": activity_data.popularity_score,
                "image_url": activity_data.image_url or "",
            },
        )
        next_activity_id += 1


def _append_row_if_missing(path: Path, match_criteria: dict, row: dict) -> None:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = list(reader.fieldnames or [])
        existing_rows = list(reader)

    if any(_row_matches(existing_row, match_criteria) for existing_row in existing_rows):
        return

    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def _row_matches(row: dict, match_criteria: dict) -> bool:
    return all((row.get(key) or "").strip() == str(value).strip() for key, value in match_criteria.items())


def _next_sequence_value(path: Path, prefix: str) -> int:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        values = []
        for row in reader:
            raw_id = row.get("id", "")
            if raw_id.startswith(prefix):
                try:
                    values.append(int(raw_id[len(prefix) :]))
                except ValueError:
                    continue
    return max(values, default=0) + 1
