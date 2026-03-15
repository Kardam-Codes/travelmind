"""
Feature: Database Seed
File Purpose: Load reference travel datasets into PostgreSQL-backed tables
Owner: Misha
Dependencies: csv, pathlib, sqlmodel
Last Updated: 2026-03-14
"""

import csv
from pathlib import Path

from sqlmodel import Session, select

from app.database.models.activity import Activity
from app.database.models.city import City
from app.database.models.hotel import Hotel
from app.database.models.place import Place
from app.database.session import engine


DATASET_DIR = Path(__file__).resolve().parents[3] / "datasets"


def _parse_bool(value: str | None) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def _parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def seed_reference_data() -> None:
    with Session(engine) as session:
        has_cities = session.exec(select(City.id).limit(1)).first()
        has_places = session.exec(select(Place.id).limit(1)).first()
        has_hotels = session.exec(select(Hotel.id).limit(1)).first()
        has_activities = session.exec(select(Activity.id).limit(1)).first()

        if has_cities and has_places and has_hotels and has_activities:
            return

        place_external_ids: dict[str, int] = {}

        if not has_cities:
            with (DATASET_DIR / "city_master_list.csv").open("r", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    city = City(
                        city=row["city"].strip(),
                        state=row["state"].strip(),
                        tier=row.get("tier"),
                        tourism_type=row.get("tourism_type"),
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        best_season=row.get("best_season"),
                        popularity_score=_parse_int(row.get("popularity_score")),
                        notes=row.get("notes"),
                        image_url=row.get("image_url"),
                        source="seed",
                        verified=True,
                    )
                    session.add(city)
            session.commit()

        if not has_places:
            with (DATASET_DIR / "places.csv").open("r", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    place = Place(
                        name=row["name"].strip(),
                        city=row["city"].strip(),
                        state=row["state"].strip(),
                        category=row["category"].strip(),
                        tags=row.get("tags"),
                        rating=_parse_float(row.get("rating")),
                        price_estimate=_parse_float(row.get("price_estimate")),
                        duration_hours=_parse_float(row.get("duration_hours")),
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        popularity_score=_parse_int(row.get("popularity_score")),
                        best_time=row.get("best_time"),
                        family_friendly=_parse_bool(row.get("family_friendly")),
                        foreign_tourist_friendly=_parse_bool(row.get("foreign_tourist_friendly")),
                        source="seed",
                        verified=True,
                    )
                    session.add(place)
                    session.flush()
                    place_external_ids[row["id"].strip()] = place.id
            session.commit()
        else:
            with (DATASET_DIR / "places.csv").open("r", encoding="utf-8") as file:
                places = session.exec(select(Place)).all()
                places_by_key = {(place.name, place.city): place.id for place in places}
                for row in csv.DictReader(file):
                    place_external_ids[row["id"].strip()] = places_by_key.get((row["name"].strip(), row["city"].strip()))

        if not has_hotels:
            with (DATASET_DIR / "hotels.csv").open("r", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    hotel = Hotel(
                        name=row["name"].strip(),
                        city=row["city"].strip(),
                        state=row["state"].strip(),
                        price_per_night=_parse_float(row.get("price_per_night")),
                        hotel_type=row.get("hotel_type"),
                        rating=_parse_float(row.get("rating")),
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        budget_category=row.get("budget_category"),
                        nearby_area=row.get("nearby_area"),
                        popularity_score=_parse_int(row.get("popularity_score")),
                        source="seed",
                        verified=True,
                    )
                    session.add(hotel)
            session.commit()

        if not has_activities:
            with (DATASET_DIR / "activities.csv").open("r", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    activity = Activity(
                        name=row["name"].strip(),
                        city=row["city"].strip(),
                        state=row["state"].strip(),
                        category=row["category"].strip(),
                        tags=row.get("tags"),
                        price=_parse_float(row.get("price")),
                        duration_hours=_parse_float(row.get("duration_hours")),
                        rating=_parse_float(row.get("rating")),
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        linked_place_id=place_external_ids.get(row.get("linked_place_id", "").strip()),
                        near_place_name=row.get("near_place_name"),
                        popularity_score=_parse_int(row.get("popularity_score")),
                        source="seed",
                        verified=True,
                    )
                    session.add(activity)
            session.commit()
