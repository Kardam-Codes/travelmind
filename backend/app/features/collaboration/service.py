from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.itinerary import ItineraryItem
from app.features.collaboration.events import save_collaboration_event
from app.features.trips.permissions import ensure_trip_member_role
from app.repositories.itinerary_repository import (
    create_itinerary_item,
    delete_itinerary_item,
    get_itinerary_by_trip_id,
    get_itinerary_item_by_id,
    persist_changes,
)
from app.repositories.trip_repository import get_trip_by_id, save_trip
from app.schemas.itinerary import ConflictResponse, ItineraryOperationRequest, ItineraryOperationResult, TripVersionRead


EDIT_EVENT_TYPES = {"ADD_ITEM", "REMOVE_ITEM", "MOVE_ITEM", "UPDATE_ITEM", "REORDER_DAY"}
LOCK_EVENT_TYPES = {"LOCK_DAY", "UNLOCK_DAY"}


def build_trip_version_read(trip) -> TripVersionRead:
    return TripVersionRead(
        trip_id=trip.id,
        version=trip.version,
        locked_by=trip.locked_by,
        locked_day_number=trip.locked_day_number,
    )


def apply_itinerary_operation(session: Session, operation: ItineraryOperationRequest):
    trip = get_trip_by_id(session, operation.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    if not str(operation.user_id).isdigit():
        raise HTTPException(status_code=401, detail="Invalid user id.")
    user_id = int(operation.user_id)

    if operation.type in EDIT_EVENT_TYPES:
        ensure_trip_member_role(session, operation.trip_id, user_id, minimum_role="editor")
    if operation.type in LOCK_EVENT_TYPES:
        ensure_trip_member_role(session, operation.trip_id, user_id, minimum_role="owner")

    if operation.type in EDIT_EVENT_TYPES and operation.base_version != trip.version:
        return ConflictResponse(
            operation_id=operation.operation_id,
            trip_id=operation.trip_id,
            current_version=trip.version,
            detail="Trip itinerary is out of date. Reload the latest plan.",
            payload=build_trip_version_read(trip).model_dump(),
        )

    if operation.type == "LOCK_DAY":
        return _lock_day(session, trip, operation)

    if operation.type == "UNLOCK_DAY":
        return _unlock_day(session, trip, operation)

    _ensure_day_is_editable(session, trip, operation)

    if operation.type == "ADD_ITEM":
        _add_item(session, operation)
    elif operation.type == "REMOVE_ITEM":
        _remove_item(session, operation)
    elif operation.type == "MOVE_ITEM":
        _move_item(session, operation)
    elif operation.type == "UPDATE_ITEM":
        _update_item(session, operation)
    elif operation.type == "REORDER_DAY":
        _reorder_day(session, operation)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported collaboration event: {operation.type}")

    _normalize_day_orders(session, operation.trip_id)
    persist_changes(session)

    trip.version += 1
    trip.locked_by = None
    trip.locked_day_number = None
    trip.locked_at = None
    save_trip(session, trip)

    event = save_collaboration_event(
        session=session,
        trip_id=operation.trip_id,
        user_id=str(operation.user_id),
        event_type=operation.type,
        payload=operation.payload.model_dump(exclude_none=True),
        operation_id=operation.operation_id,
        base_version=operation.base_version,
        status="applied",
    )

    return ItineraryOperationResult(
        type="ITINERARY_APPLIED",
        operation_id=operation.operation_id,
        trip_id=operation.trip_id,
        user_id=operation.user_id,
        base_version=operation.base_version,
        current_version=trip.version,
        status="applied",
        payload={
            "event_type": operation.type,
            "event_id": event.id,
            "trip_version": build_trip_version_read(trip).model_dump(),
        },
    )


def _lock_day(session: Session, trip, operation: ItineraryOperationRequest):
    day_number = operation.payload.day_number
    if day_number is None:
        raise HTTPException(status_code=400, detail="day_number is required for LOCK_DAY.")

    if trip.locked_day_number and trip.locked_by != operation.user_id and trip.locked_day_number != day_number:
        return ConflictResponse(
            operation_id=operation.operation_id,
            trip_id=operation.trip_id,
            current_version=trip.version,
            detail="Another editor is currently modifying a day.",
            payload=build_trip_version_read(trip).model_dump(),
        )

    trip.locked_by = operation.user_id
    trip.locked_day_number = day_number
    trip.locked_at = datetime.utcnow()
    save_trip(session, trip)
    save_collaboration_event(
        session=session,
        trip_id=operation.trip_id,
        user_id=operation.user_id,
        event_type=operation.type,
        payload=operation.payload.model_dump(exclude_none=True),
        operation_id=operation.operation_id,
        base_version=operation.base_version,
        status="applied",
    )
    return {
        "type": "DAY_LOCK_CHANGED",
        "trip_id": operation.trip_id,
        "user_id": operation.user_id,
        "payload": build_trip_version_read(trip).model_dump(),
    }


def _unlock_day(session: Session, trip, operation: ItineraryOperationRequest):
    if trip.locked_by and trip.locked_by != operation.user_id:
        return ConflictResponse(
            operation_id=operation.operation_id,
            trip_id=operation.trip_id,
            current_version=trip.version,
            detail="Only the user holding the lock can unlock this day.",
            payload=build_trip_version_read(trip).model_dump(),
        )

    trip.locked_by = None
    trip.locked_day_number = None
    trip.locked_at = None
    save_trip(session, trip)
    save_collaboration_event(
        session=session,
        trip_id=operation.trip_id,
        user_id=operation.user_id,
        event_type=operation.type,
        payload=operation.payload.model_dump(exclude_none=True),
        operation_id=operation.operation_id,
        base_version=operation.base_version,
        status="applied",
    )
    return {
        "type": "DAY_LOCK_CHANGED",
        "trip_id": operation.trip_id,
        "user_id": operation.user_id,
        "payload": build_trip_version_read(trip).model_dump(),
    }


def _ensure_day_is_editable(session: Session, trip, operation: ItineraryOperationRequest):
    target_day = operation.payload.day_number or operation.payload.target_day_number
    if target_day is None and operation.payload.item_id is not None:
        item = _require_item(session, operation.payload.item_id)
        target_day = item.day_number
    if trip.locked_day_number and trip.locked_by != operation.user_id and trip.locked_day_number == target_day:
        raise HTTPException(status_code=409, detail="This day is currently locked by another editor.")


def _add_item(session: Session, operation: ItineraryOperationRequest):
    if operation.payload.day_number is None or not operation.payload.title:
        raise HTTPException(status_code=400, detail="day_number and title are required for ADD_ITEM.")

    items = get_itinerary_by_trip_id(session, operation.trip_id)
    same_day_items = [item for item in items if item.day_number == operation.payload.day_number]
    item_order = operation.payload.target_item_order or len(same_day_items) + 1
    create_itinerary_item(
        session,
        ItineraryItem(
            trip_id=operation.trip_id,
            day_number=operation.payload.day_number,
            item_order=item_order,
            item_type=operation.payload.item_type or "note",
            title=operation.payload.title,
            description=operation.payload.description,
        ),
    )


def _remove_item(session: Session, operation: ItineraryOperationRequest):
    item = _require_item(session, operation.payload.item_id)
    delete_itinerary_item(session, item)


def _move_item(session: Session, operation: ItineraryOperationRequest):
    item = _require_item(session, operation.payload.item_id)
    item.day_number = operation.payload.target_day_number or item.day_number
    item.item_order = operation.payload.target_item_order or item.item_order
    session.add(item)


def _update_item(session: Session, operation: ItineraryOperationRequest):
    item = _require_item(session, operation.payload.item_id)
    if operation.payload.title is not None:
        item.title = operation.payload.title
    if operation.payload.description is not None:
        item.description = operation.payload.description
    session.add(item)


def _reorder_day(session: Session, operation: ItineraryOperationRequest):
    if operation.payload.day_number is None or not operation.payload.ordered_item_ids:
        raise HTTPException(status_code=400, detail="day_number and ordered_item_ids are required for REORDER_DAY.")

    for index, item_id in enumerate(operation.payload.ordered_item_ids, start=1):
        item = _require_item(session, item_id)
        item.day_number = operation.payload.day_number
        item.item_order = index
        session.add(item)


def _normalize_day_orders(session: Session, trip_id: int):
    items = get_itinerary_by_trip_id(session, trip_id)
    items_by_day: dict[int, list] = {}
    for item in items:
        items_by_day.setdefault(item.day_number, []).append(item)

    for day_items in items_by_day.values():
        for index, item in enumerate(sorted(day_items, key=lambda value: (value.item_order, value.id)), start=1):
            item.item_order = index
            session.add(item)


def _require_item(session: Session, item_id: int | None):
    if item_id is None:
        raise HTTPException(status_code=400, detail="item_id is required.")
    item = get_itinerary_item_by_id(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found.")
    return item
