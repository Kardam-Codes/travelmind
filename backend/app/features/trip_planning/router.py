from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.session import get_session
from app.core.security import get_current_org_id, get_current_user_id
from app.features.trip_planning.query_service import build_trip_dashboard, create_trip_from_query
from app.features.trip_planning.service import create_trip_plan, fetch_all_trips
from app.features.trips.permissions import ensure_org_member, ensure_trip_member_role, require_trip
from app.repositories.trip_member_repository import create_trip_member, list_trip_members, update_trip_member, get_trip_member
from app.database.models.trip_member import TripMember
from app.schemas.trip import TripCreate, TripDashboardResponse, TripGenerationResponse, TripQueryRequest, TripRead
from app.schemas.trip_member import TripMemberCreate, TripMemberRead, TripMemberUpdate


router = APIRouter(prefix="/trips", tags=["Trip Planning"])


@router.post("/", response_model=TripRead)
def create_trip_endpoint(
    trip_data: TripCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    return create_trip_plan(session, trip_data, org_id, user_id)


@router.post("/generate-from-query", response_model=TripGenerationResponse)
def create_trip_from_query_endpoint(
    payload: TripQueryRequest,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    return create_trip_from_query(session, payload.query, org_id, user_id)


@router.get("/", response_model=List[TripRead])
def get_all_trips_endpoint(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    return fetch_all_trips(session, org_id)


@router.get("/{trip_id}", response_model=TripRead)
def get_trip_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    trip = require_trip(session, trip_id, org_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    return trip


@router.get("/{trip_id}/dashboard", response_model=TripDashboardResponse)
def get_trip_dashboard_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    trip = require_trip(session, trip_id, org_id)
    membership = ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    return build_trip_dashboard(session, trip, membership.role)


@router.get("/{trip_id}/members", response_model=list[TripMemberRead])
def list_trip_members_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="viewer")
    members = list_trip_members(session, trip_id)
    return [TripMemberRead(id=member.id, trip_id=member.trip_id, user_id=member.user_id, role=member.role) for member in members]


@router.post("/{trip_id}/members", response_model=TripMemberRead)
def add_trip_member_endpoint(
    trip_id: int,
    payload: TripMemberCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="owner")
    existing = get_trip_member(session, trip_id, payload.user_id)
    if existing:
        existing.role = payload.role
        member = update_trip_member(session, existing)
    else:
        member = create_trip_member(session, TripMember(trip_id=trip_id, user_id=payload.user_id, role=payload.role))
    return TripMemberRead(id=member.id, trip_id=member.trip_id, user_id=member.user_id, role=member.role)


@router.patch("/{trip_id}/members/{member_user_id}", response_model=TripMemberRead)
def update_trip_member_endpoint(
    trip_id: int,
    member_user_id: int,
    payload: TripMemberUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    ensure_trip_member_role(session, trip_id, user_id, minimum_role="owner")
    member = get_trip_member(session, trip_id, member_user_id)
    if not member:
        raise HTTPException(status_code=404, detail="Trip member not found.")
    member.role = payload.role
    member = update_trip_member(session, member)
    return TripMemberRead(id=member.id, trip_id=member.trip_id, user_id=member.user_id, role=member.role)
