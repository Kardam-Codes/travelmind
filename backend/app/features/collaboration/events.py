import json
from sqlmodel import Session

from app.database.models.collaboration import CollaborationEvent


def save_collaboration_event(
    session: Session,
    trip_id: int,
    user_id: str,
    event_type: str,
    payload: dict | None = None,
) -> CollaborationEvent:
    event = CollaborationEvent(
        trip_id=trip_id,
        user_id=user_id,
        event_type=event_type,
        payload=json.dumps(payload) if payload else None,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
