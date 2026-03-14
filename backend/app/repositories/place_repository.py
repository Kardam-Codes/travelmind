from typing import List, Optional
from sqlmodel import Session, select
from app.database.models.place import Place


def get_place_by_id(session: Session, place_id: int) -> Optional[Place]:
    statement = select(Place).where(Place.id == place_id)
    return session.exec(statement).first()


def get_places_by_city(session: Session, city_name: str) -> List[Place]:
    statement = select(Place).where(Place.city == city_name).order_by(Place.rating.desc())
    return list(session.exec(statement).all())


def get_places_by_filters(
    session: Session,
    city_name: str,
    category: Optional[str] = None,
    min_rating: Optional[float] = None,
) -> List[Place]:
    statement = select(Place).where(Place.city == city_name)

    if category:
        statement = statement.where(Place.category == category)

    if min_rating is not None:
        statement = statement.where(Place.rating >= min_rating)

    statement = statement.order_by(Place.popularity_score.desc())
    return list(session.exec(statement).all())


def create_place(session: Session, place_data: Place) -> Place:
    session.add(place_data)
    session.commit()
    session.refresh(place_data)
    return place_data
