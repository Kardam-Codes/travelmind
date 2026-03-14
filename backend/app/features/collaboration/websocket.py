from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session

from app.core.security import decode_access_token
from app.features.collaboration.events import save_collaboration_event
from app.features.collaboration.manager import manager
from app.features.collaboration.service import apply_itinerary_operation, build_trip_version_read
from app.repositories.trip_repository import get_trip_by_id
from app.features.trips.permissions import ensure_trip_member_role
from app.schemas.itinerary import ConflictResponse, ItineraryOperationRequest


async def handle_trip_websocket(websocket: WebSocket, trip_id: int, session: Session):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    user_id = decode_access_token(token)
    membership = ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    await manager.connect(trip_id, websocket, user_id=str(user_id))

    trip = get_trip_by_id(session, trip_id)
    if trip:
        await websocket.send_json(
            {
                "type": "SYNC_SNAPSHOT",
                "trip_id": trip_id,
                "user_id": str(user_id),
                "payload": build_trip_version_read(trip).model_dump(),
            }
        )

    await manager.broadcast(
        trip_id,
        {
            "type": "USER_PRESENCE",
            "trip_id": trip_id,
            "user_id": str(user_id),
            "payload": {"active_users": manager.list_users(trip_id)},
        },
    )

    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type", "SYNC_STATE")
            payload = data.get("payload", {})

            if event_type == "CHAT_MESSAGE":
                ensure_trip_member_role(session, trip_id, user_id, minimum_role="editor")
                save_collaboration_event(
                    session=session,
                    trip_id=trip_id,
                    user_id=str(user_id),
                    event_type=event_type,
                    payload=payload,
                    status="applied",
                )
                await manager.broadcast(
                    trip_id,
                    {
                        "type": event_type,
                        "trip_id": trip_id,
                        "user_id": str(user_id),
                        "payload": payload,
                    },
                )
                continue

            if event_type in {"ADD_ITEM", "REMOVE_ITEM", "MOVE_ITEM", "UPDATE_ITEM", "REORDER_DAY", "LOCK_DAY", "UNLOCK_DAY"}:
                ensure_trip_member_role(session, trip_id, user_id, minimum_role="editor")
                operation = ItineraryOperationRequest.model_validate(
                    {
                        "type": event_type,
                        "operation_id": data.get("operation_id"),
                        "trip_id": trip_id,
                        "user_id": str(user_id),
                        "base_version": data.get("base_version"),
                        "payload": payload,
                    }
                )
                result = apply_itinerary_operation(session, operation)
                message = result.model_dump() if isinstance(result, ConflictResponse) else result.model_dump() if hasattr(result, "model_dump") else result
                await manager.broadcast(trip_id, message)
                continue

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
        manager.disconnect(trip_id, websocket, user_id=user_id)
        await manager.broadcast(
            trip_id,
            {
                "type": "USER_PRESENCE",
                "trip_id": trip_id,
                "user_id": user_id,
                "payload": {"active_users": manager.list_users(trip_id)},
            },
        )
