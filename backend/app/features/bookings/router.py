from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.core.security import get_current_org_id, get_current_user_id
from app.database.session import get_session
from app.features.bookings.service import add_offer, create_request, list_offers, list_requests, log_click, update_request
from app.repositories.booking_repository import get_booking_request
from app.features.trips.permissions import ensure_org_member, ensure_org_admin, ensure_trip_member_role, require_trip
from app.schemas.booking import (
    BookingOfferCreate,
    BookingOfferRead,
    BookingRequestCreate,
    BookingRequestRead,
    BookingRequestUpdate,
)


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/requests", response_model=BookingRequestRead)
def create_booking_request_endpoint(
    payload: BookingRequestCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    require_trip(session, payload.trip_id, org_id)
    ensure_trip_member_role(session, payload.trip_id, user_id, minimum_role="viewer")
    request = create_request(
        session=session,
        org_id=org_id,
        trip_id=payload.trip_id,
        requester_id=user_id,
        traveler_name=payload.traveler_name,
        traveler_email=payload.traveler_email,
        traveler_phone=payload.traveler_phone,
        total_travelers=payload.total_travelers,
        budget_total=payload.budget_total,
        notes=payload.notes,
    )
    return BookingRequestRead(**request.model_dump())


@router.get("/requests", response_model=list[BookingRequestRead])
def list_booking_requests_endpoint(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    requests = list_requests(session, org_id)
    return [BookingRequestRead(**request.model_dump()) for request in requests]


@router.patch("/requests/{request_id}", response_model=BookingRequestRead)
def update_booking_request_endpoint(
    request_id: int,
    payload: BookingRequestUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_admin(session, org_id, user_id)
    request = get_booking_request(session, request_id)
    if not request or request.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Booking request not found.")
    request = update_request(session, request_id, payload.status, payload.assigned_agent_id)
    return BookingRequestRead(**request.model_dump())


@router.post("/requests/{request_id}/offers", response_model=BookingOfferRead)
def create_booking_offer_endpoint(
    request_id: int,
    payload: BookingOfferCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    request = get_booking_request(session, request_id)
    if not request or request.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Booking request not found.")
    offer = add_offer(session, request_id, payload.provider, payload.deeplink_url, payload.price, payload.commission_rate)
    return BookingOfferRead(**offer.model_dump())


@router.get("/requests/{request_id}/offers", response_model=list[BookingOfferRead])
def list_booking_offers_endpoint(
    request_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    request = get_booking_request(session, request_id)
    if not request or request.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Booking request not found.")
    offers = list_offers(session, request_id)
    return [BookingOfferRead(**offer.model_dump()) for offer in offers]


@router.get("/offers/{offer_id}/redirect")
def redirect_offer_endpoint(
    offer_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    referrer: str | None = Header(None),
):
    offer = log_click(session, offer_id, user_id, referrer)
    return RedirectResponse(offer.deeplink_url, status_code=302)
