import json
from sqlmodel import Session

from app.database.models.collaboration import CollaborationEvent


def save_collaboration_event(
    session: Session,
    trip_id: int,
    user_id: str,
    event_type: str,
    payload: dict | None = None,
    operation_id: str | None = None,
    base_version: int | None = None,
    status: str = "applied",
) -> CollaborationEvent:
    event = CollaborationEvent(
        trip_id=trip_id,
        user_id=user_id,
        operation_id=operation_id,
        base_version=base_version,
        event_type=event_type,
        status=status,
        payload=json.dumps(payload) if payload else None,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
