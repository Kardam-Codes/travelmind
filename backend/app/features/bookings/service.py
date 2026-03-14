from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.booking import BookingClick, BookingOffer, BookingRequest
from app.repositories.booking_repository import (
    create_booking_click,
    create_booking_offer,
    create_booking_request,
    get_booking_offer,
    get_booking_request,
    list_booking_offers,
    list_booking_requests,
    update_booking_request,
)


def create_request(
    session: Session,
    org_id: int,
    trip_id: int,
    requester_id: int,
    traveler_name: str,
    traveler_email: str,
    traveler_phone: str | None,
    total_travelers: int,
    budget_total: float | None,
    notes: str | None,
):
    request = BookingRequest(
        organization_id=org_id,
        trip_id=trip_id,
        requester_id=requester_id,
        traveler_name=traveler_name,
        traveler_email=traveler_email,
        traveler_phone=traveler_phone,
        total_travelers=total_travelers,
        budget_total=budget_total,
        notes=notes,
    )
    return create_booking_request(session, request)


def list_requests(session: Session, org_id: int):
    return list_booking_requests(session, org_id)


def update_request(session: Session, request_id: int, status: str | None, assigned_agent_id: int | None):
    request = get_booking_request(session, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Booking request not found.")
    if status:
        request.status = status
    if assigned_agent_id is not None:
        request.assigned_agent_id = assigned_agent_id
    return update_booking_request(session, request)


def add_offer(session: Session, request_id: int, provider: str, deeplink_url: str, price: float, commission_rate: float):
    request = get_booking_request(session, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Booking request not found.")
    offer = BookingOffer(
        request_id=request_id,
        provider=provider,
        deeplink_url=deeplink_url,
        price=price,
        commission_rate=commission_rate,
    )
    return create_booking_offer(session, offer)


def list_offers(session: Session, request_id: int):
    return list_booking_offers(session, request_id)


def log_click(session: Session, offer_id: int, user_id: int | None, referrer: str | None):
    offer = get_booking_offer(session, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Booking offer not found.")
    click = BookingClick(offer_id=offer_id, user_id=user_id, referrer=referrer)
    create_booking_click(session, click)
    return offer
