import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.invite import Invite
from app.repositories.invite_repository import create_invite, get_invite_by_token, update_invite
from app.features.orgs.service import ensure_org_admin
from app.repositories.trip_member_repository import create_trip_member, get_trip_member
from app.features.trips.permissions import ensure_trip_member_role
from app.repositories.org_member_repository import create_org_member, get_org_member
from app.database.models.org_member import OrgMember
from app.database.models.trip_member import TripMember


def create_invite_for_org(
    session: Session,
    email: str,
    org_id: int,
    role: str,
    inviter_id: int,
    expires_in_hours: int,
) -> Invite:
    ensure_org_admin(session, org_id, inviter_id)
    invite = Invite(
        token=secrets.token_urlsafe(16),
        email=email.lower(),
        scope="org",
        organization_id=org_id,
        role=role,
        inviter_id=inviter_id,
        expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
    )
    return create_invite(session, invite)


def create_invite_for_trip(
    session: Session,
    email: str,
    trip_id: int,
    role: str,
    inviter_id: int,
    expires_in_hours: int,
) -> Invite:
    ensure_trip_member_role(session, trip_id, inviter_id, minimum_role="owner")
    invite = Invite(
        token=secrets.token_urlsafe(16),
        email=email.lower(),
        scope="trip",
        trip_id=trip_id,
        role=role,
        inviter_id=inviter_id,
        expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
    )
    return create_invite(session, invite)


def accept_invite(session: Session, token: str, user_id: int, user_email: str) -> Invite:
    invite = get_invite_by_token(session, token)
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found.")
    if invite.status != "pending":
        raise HTTPException(status_code=400, detail="Invite is no longer active.")
    if invite.expires_at and invite.expires_at < datetime.utcnow():
        invite.status = "expired"
        update_invite(session, invite)
        raise HTTPException(status_code=400, detail="Invite has expired.")
    if invite.email and invite.email != user_email.lower():
        raise HTTPException(status_code=403, detail="Invite email does not match.")

    if invite.scope == "org":
        if invite.organization_id is None:
            raise HTTPException(status_code=400, detail="Invite is missing organization.")
        existing = get_org_member(session, invite.organization_id, user_id)
        if not existing:
            create_org_member(session, OrgMember(organization_id=invite.organization_id, user_id=user_id, role=invite.role))
    elif invite.scope == "trip":
        if invite.trip_id is None:
            raise HTTPException(status_code=400, detail="Invite is missing trip.")
        existing = get_trip_member(session, invite.trip_id, user_id)
        if not existing:
            create_trip_member(session, TripMember(trip_id=invite.trip_id, user_id=user_id, role=invite.role))
    else:
        raise HTTPException(status_code=400, detail="Invalid invite scope.")

    invite.status = "accepted"
    return update_invite(session, invite)
