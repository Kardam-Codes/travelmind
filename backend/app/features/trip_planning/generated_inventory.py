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
    existing_city = session.exec(select(City).where(City.city == city_data.city)).first()
    if existing_city:
        return existing_city

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
        source=city_pack.provider,
        verified=False,
    )
    session.add(city)
    session.commit()
    session.refresh(city)

    place_name_to_id: dict[str, int] = {}
    for place_data in city_pack.places:
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
            source=city_pack.provider,
            verified=False,
        )
        session.add(place)
        session.flush()
        place_name_to_id[place.name] = place.id

    for hotel_data in city_pack.hotels:
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
                source=city_pack.provider,
                verified=False,
            )
        )

    for activity_data in city_pack.activities:
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
                source=city_pack.provider,
                verified=False,
            )
        )

    session.commit()
    _append_city_pack_to_datasets(city_pack)
    return city


def _append_city_pack_to_datasets(city_pack: GenerateCityPackResponse) -> None:
    city = city_pack.city
    _append_row_if_missing(
        DATASET_DIR / "city_master_list.csv",
        key_column="city",
        key_value=city.city,
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
            key_column="name",
            key_value=place_data.name,
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
            key_column="name",
            key_value=hotel_data.name,
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
            key_column="name",
            key_value=activity_data.name,
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
            },
        )
        next_activity_id += 1


def _append_row_if_missing(path: Path, key_column: str, key_value: str, row: dict) -> None:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = list(reader.fieldnames or [])
        existing_rows = list(reader)

    if any(existing_row.get(key_column) == key_value for existing_row in existing_rows):
        return

    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({field: row.get(field, "") for field in fieldnames})


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
