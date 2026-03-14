from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.trip_member_repository import create_trip_member, get_trip_member
from app.repositories.org_member_repository import get_org_member
from app.repositories.trip_repository import get_trip_by_id
from app.database.models.trip_member import TripMember


TRIP_ROLE_RANK = {"viewer": 0, "editor": 1, "owner": 2}
ORG_ADMIN_ROLES = {"owner", "admin"}


def ensure_org_member(session: Session, org_id: int, user_id: int):
    member = get_org_member(session, org_id, user_id)
    if not member:
        raise HTTPException(status_code=403, detail="User does not belong to this organization.")
    return member


def ensure_org_admin(session: Session, org_id: int, user_id: int):
    member = ensure_org_member(session, org_id, user_id)
    if member.role not in ORG_ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Org admin privileges required.")
    return member


def ensure_trip_member_role(session: Session, trip_id: int, user_id: int, minimum_role: str = "viewer"):
    member = get_trip_member(session, trip_id, user_id)
    if not member:
        trip = get_trip_by_id(session, trip_id)
        if trip:
            org_member = get_org_member(session, trip.organization_id, user_id)
            if org_member:
                inferred_role = "owner" if org_member.role in ORG_ADMIN_ROLES else "viewer"
                member = create_trip_member(session, TripMember(trip_id=trip_id, user_id=user_id, role=inferred_role))
    if not member:
        raise HTTPException(status_code=403, detail="User does not belong to this trip.")
    if TRIP_ROLE_RANK.get(member.role, -1) < TRIP_ROLE_RANK.get(minimum_role, 0):
        raise HTTPException(status_code=403, detail="Insufficient trip permissions.")
    return member


def ensure_trip_owner_or_admin(session: Session, trip_id: int, user_id: int):
    member = ensure_trip_member_role(session, trip_id, user_id, minimum_role="owner")
    return member


def require_trip(session: Session, trip_id: int, org_id: int):
    trip = get_trip_by_id(session, trip_id)
    if not trip or trip.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Trip not found.")
    return trip
