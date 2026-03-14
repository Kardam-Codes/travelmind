import json

from fastapi import APIRouter, Depends, WebSocket
from sqlmodel import Session

from app.database.session import get_session
from app.core.security import get_current_org_id, get_current_user_id
from app.features.trips.permissions import ensure_org_member, ensure_trip_member_role
from app.repositories.collaboration_repository import get_events_by_trip_id
from app.features.collaboration.websocket import handle_trip_websocket
from app.schemas.collaboration import CollaborationEventRead


router = APIRouter(tags=["Collaboration"])


@router.get("/collaboration/{trip_id}/events", response_model=list[CollaborationEventRead])
def get_trip_collaboration_events(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    events = get_events_by_trip_id(session, trip_id)
    return [
        CollaborationEventRead(
            id=event.id,
            trip_id=event.trip_id,
            user_id=event.user_id,
            operation_id=event.operation_id,
            base_version=event.base_version,
            event_type=event.event_type,
            status=event.status,
            payload=json.dumps(json.loads(event.payload)) if event.payload else None,
            created_at=event.created_at.isoformat(),
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
