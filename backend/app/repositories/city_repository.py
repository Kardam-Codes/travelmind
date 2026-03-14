from typing import List, Optional
from sqlmodel import Session, select
from app.database.models.city import City


def get_all_cities(session: Session) -> List[City]:
    statement = select(City).order_by(City.city)
    return list(session.exec(statement).all())


def get_city_by_name(session: Session, city_name: str) -> Optional[City]:
    statement = select(City).where(City.city == city_name)
    return session.exec(statement).first()


def create_city(session: Session, city_data: City) -> City:
    session.add(city_data)
    session.commit()
    session.refresh(city_data)
    return city_data
