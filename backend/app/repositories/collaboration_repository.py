from typing import List

from sqlmodel import Session, select

from app.database.models.collaboration import CollaborationEvent


def get_events_by_trip_id(session: Session, trip_id: int) -> List[CollaborationEvent]:
    statement = (
        select(CollaborationEvent)
        .where(CollaborationEvent.trip_id == trip_id)
        .order_by(CollaborationEvent.id.asc())
    )
    return list(session.exec(statement).all())
