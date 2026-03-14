from typing import List, Optional
from sqlmodel import Session, select
from app.database.models.hotel import Hotel


def get_hotel_by_id(session: Session, hotel_id: int) -> Optional[Hotel]:
    statement = select(Hotel).where(Hotel.id == hotel_id)
    return session.exec(statement).first()


def get_hotels_by_city(session: Session, city_name: str) -> List[Hotel]:
    statement = select(Hotel).where(Hotel.city == city_name).order_by(Hotel.rating.desc())
    return list(session.exec(statement).all())


def get_hotels_by_filters(
    session: Session,
    city_name: str,
    budget_category: Optional[str] = None,
    hotel_type: Optional[str] = None,
) -> List[Hotel]:
    statement = select(Hotel).where(Hotel.city == city_name)

    if budget_category:
        statement = statement.where(Hotel.budget_category == budget_category)

    if hotel_type:
        statement = statement.where(Hotel.hotel_type == hotel_type)

    statement = statement.order_by(Hotel.popularity_score.desc())
    return list(session.exec(statement).all())


def create_hotel(session: Session, hotel_data: Hotel) -> Hotel:
    session.add(hotel_data)
    session.commit()
    session.refresh(hotel_data)
    return hotel_data
