from datetime import datetime

from sqlmodel import Session, select

from app.database.models.booking import BookingClick, BookingOffer, BookingRequest
from app.database.models.trip import Trip
from app.schemas.report import AgencyReport, BookingKPI, TopDestination


def build_agency_report(session: Session, org_id: int, start: datetime | None, end: datetime | None) -> AgencyReport:
    request_query = select(BookingRequest).where(BookingRequest.organization_id == org_id)
    offer_query = select(BookingOffer)
    click_query = select(BookingClick)
    trip_query = select(Trip).where(Trip.organization_id == org_id)

    if start:
        request_query = request_query.where(BookingRequest.created_at >= start)
        offer_query = offer_query.where(BookingOffer.created_at >= start)
        click_query = click_query.where(BookingClick.created_at >= start)
        trip_query = trip_query.where(Trip.id >= 0)
    if end:
        request_query = request_query.where(BookingRequest.created_at <= end)
        offer_query = offer_query.where(BookingOffer.created_at <= end)
        click_query = click_query.where(BookingClick.created_at <= end)
        trip_query = trip_query.where(Trip.id >= 0)

    requests = list(session.exec(request_query).all())
    request_ids = {request.id for request in requests}
    offers = [offer for offer in session.exec(offer_query).all() if offer.request_id in request_ids]
    offer_ids = {offer.id for offer in offers}
    clicks = [click for click in session.exec(click_query).all() if click.offer_id in offer_ids]
    trips = list(session.exec(trip_query).all())

    commission_total = sum(offer.price * offer.commission_rate for offer in offers)
    conversion_rate = (len(clicks) / len(offers)) if offers else 0.0

    top_destinations_map: dict[str, int] = {}
    for trip in trips:
        top_destinations_map[trip.destination_city] = top_destinations_map.get(trip.destination_city, 0) + 1

    top_destinations = [
        TopDestination(destination_city=city, count=count)
        for city, count in sorted(top_destinations_map.items(), key=lambda item: item[1], reverse=True)[:5]
    ]

    return AgencyReport(
        kpis=BookingKPI(
            total_requests=len(requests),
            total_offers=len(offers),
            total_clicks=len(clicks),
            total_commission=commission_total,
            conversion_rate=conversion_rate,
        ),
        top_destinations=top_destinations,
    )
