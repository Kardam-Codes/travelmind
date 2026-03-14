from typing import List, Optional

from sqlmodel import Session, select

from app.database.models.booking import BookingClick, BookingOffer, BookingRequest


def create_booking_request(session: Session, request: BookingRequest) -> BookingRequest:
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def update_booking_request(session: Session, request: BookingRequest) -> BookingRequest:
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


def get_booking_request(session: Session, request_id: int) -> Optional[BookingRequest]:
    statement = select(BookingRequest).where(BookingRequest.id == request_id)
    return session.exec(statement).first()


def list_booking_requests(session: Session, org_id: int) -> List[BookingRequest]:
    statement = select(BookingRequest).where(BookingRequest.organization_id == org_id).order_by(BookingRequest.id.desc())
    return list(session.exec(statement).all())


def create_booking_offer(session: Session, offer: BookingOffer) -> BookingOffer:
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def list_booking_offers(session: Session, request_id: int) -> List[BookingOffer]:
    statement = select(BookingOffer).where(BookingOffer.request_id == request_id).order_by(BookingOffer.id.desc())
    return list(session.exec(statement).all())


def get_booking_offer(session: Session, offer_id: int) -> Optional[BookingOffer]:
    statement = select(BookingOffer).where(BookingOffer.id == offer_id)
    return session.exec(statement).first()


def create_booking_click(session: Session, click: BookingClick) -> BookingClick:
    session.add(click)
    session.commit()
    session.refresh(click)
    return click


def list_booking_clicks(session: Session, offer_id: int) -> List[BookingClick]:
    statement = select(BookingClick).where(BookingClick.offer_id == offer_id).order_by(BookingClick.id.desc())
    return list(session.exec(statement).all())
