from typing import List
from sqlmodel import Session, select
from app.database.models.itinerary import ItineraryItem


def create_itinerary_item(session: Session, item_data: ItineraryItem) -> ItineraryItem:
    session.add(item_data)
    session.commit()
    session.refresh(item_data)
    return item_data


def get_itinerary_by_trip_id(session: Session, trip_id: int) -> List[ItineraryItem]:
    statement = (
        select(ItineraryItem)
        .where(ItineraryItem.trip_id == trip_id)
        .order_by(ItineraryItem.day_number, ItineraryItem.item_order)
    )
    return list(session.exec(statement).all())


def delete_itinerary_by_trip_id(session: Session, trip_id: int) -> None:
    items = get_itinerary_by_trip_id(session, trip_id)
    for item in items:
        session.delete(item)
    session.commit()
