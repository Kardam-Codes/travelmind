from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session

from app.features.collaboration.events import save_collaboration_event
from app.features.collaboration.manager import manager


async def handle_trip_websocket(websocket: WebSocket, trip_id: int, session: Session):
    await manager.connect(trip_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type", "SYNC_STATE")
            user_id = data.get("user_id", "anonymous")
            payload = data.get("payload", {})

            save_collaboration_event(
                session=session,
                trip_id=trip_id,
                user_id=user_id,
                event_type=event_type,
                payload=payload,
            )

            await manager.broadcast(
                trip_id,
                {
                    "type": event_type,
                    "trip_id": trip_id,
                    "user_id": user_id,
                    "payload": payload,
                },
            )
    except WebSocketDisconnect:
        manager.disconnect(trip_id, websocket)
