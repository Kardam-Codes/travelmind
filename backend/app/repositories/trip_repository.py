from typing import List, Optional
from sqlmodel import Session, select
from app.database.models.trip import Trip


def create_trip(session: Session, trip_data: Trip) -> Trip:
    session.add(trip_data)
    session.commit()
    session.refresh(trip_data)
    return trip_data


def get_trip_by_id(session: Session, trip_id: int) -> Optional[Trip]:
    statement = select(Trip).where(Trip.id == trip_id)
    return session.exec(statement).first()


def get_all_trips(session: Session) -> List[Trip]:
    statement = select(Trip).order_by(Trip.id.desc())
    return list(session.exec(statement).all())
