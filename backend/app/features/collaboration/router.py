from fastapi import APIRouter, Depends, WebSocket
from sqlmodel import Session

from app.database.session import get_session
from app.features.collaboration.websocket import handle_trip_websocket


router = APIRouter(tags=["Collaboration"])


@router.websocket("/ws/trip/{trip_id}")
async def trip_collaboration_socket(
    websocket: WebSocket,
    trip_id: int,
    session: Session = Depends(get_session),
):
    await handle_trip_websocket(websocket, trip_id, session)
