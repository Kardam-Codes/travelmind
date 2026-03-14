import json

from fastapi import APIRouter, Depends, WebSocket
from sqlmodel import Session

from app.database.session import get_session
from app.repositories.collaboration_repository import get_events_by_trip_id
from app.features.collaboration.websocket import handle_trip_websocket
from app.schemas.collaboration import CollaborationEventRead


router = APIRouter(tags=["Collaboration"])


@router.get("/collaboration/{trip_id}/events", response_model=list[CollaborationEventRead])
def get_trip_collaboration_events(trip_id: int, session: Session = Depends(get_session)):
    events = get_events_by_trip_id(session, trip_id)
    return [
        CollaborationEventRead(
            id=event.id,
            trip_id=event.trip_id,
            user_id=event.user_id,
            event_type=event.event_type,
            payload=json.dumps(json.loads(event.payload)) if event.payload else None,
        )
        for event in events
    ]


@router.websocket("/ws/trip/{trip_id}")
async def trip_collaboration_socket(
    websocket: WebSocket,
    trip_id: int,
    session: Session = Depends(get_session),
):
    await handle_trip_websocket(websocket, trip_id, session)
