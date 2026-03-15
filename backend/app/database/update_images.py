"""
Manual image_url updater for cities, places, and activities.

Usage:
  set DATABASE_URL=<your_db_url>
  python -m app.database.update_images
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

from sqlmodel import Session, create_engine, select

from app.database.models.activity import Activity
from app.database.models.city import City
from app.database.models.place import Place


ROOT = Path(__file__).resolve().parents[2]
DATASETS = ROOT / "datasets"
CITY_CSV = DATASETS / "city_master_list.csv"
ACTIVITY_CSV = DATASETS / "activities.csv"
PLACE_CSV = DATASETS / "places.csv"


def _load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is not set.")

    engine = create_engine(database_url)

    city_rows = _load_rows(CITY_CSV)
    activity_rows = _load_rows(ACTIVITY_CSV)
    place_rows = _load_rows(PLACE_CSV)

    updated_cities = 0
    updated_activities = 0
    updated_places = 0

    with Session(engine) as session:
        for row in city_rows:
            name = (row.get("city") or "").strip()
            image_url = (row.get("image_url") or "").strip()
            if not name or not image_url:
                continue
            city = session.exec(select(City).where(City.city == name)).first()
            if city and city.image_url != image_url:
                city.image_url = image_url
                session.add(city)
                updated_cities += 1

        for row in activity_rows:
            name = (row.get("name") or "").strip()
            city_name = (row.get("city") or "").strip()
            image_url = (row.get("image_url") or "").strip()
            if not name or not city_name or not image_url:
                continue
            activity = session.exec(
                select(Activity).where(Activity.name == name).where(Activity.city == city_name)
            ).first()
            if activity and activity.image_url != image_url:
                activity.image_url = image_url
                session.add(activity)
                updated_activities += 1

        for row in place_rows:
            name = (row.get("name") or "").strip()
            city_name = (row.get("city") or "").strip()
            state = (row.get("state") or "").strip()
            image_url = (row.get("image_url") or "").strip()
            if not name or not city_name or not image_url:
                continue
            place = session.exec(
                select(Place)
                .where(Place.name == name)
                .where(Place.city == city_name)
                .where(Place.state == state)
            ).first()
            if place and place.image_url != image_url:
                place.image_url = image_url
                session.add(place)
                updated_places += 1

        session.commit()

    print(f"Updated cities: {updated_cities}")
    print(f"Updated activities: {updated_activities}")
    print(f"Updated places: {updated_places}")


if __name__ == "__main__":
    main()
