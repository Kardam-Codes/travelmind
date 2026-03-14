from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.security import get_current_user
from app.database.session import get_session
from app.features.invites.service import accept_invite, create_invite_for_org, create_invite_for_trip
from app.repositories.invite_repository import get_invite_by_token
from app.schemas.invite import InviteAcceptRequest, InviteCreate, InviteRead


router = APIRouter(prefix="/invites", tags=["Invites"])


@router.post("/", response_model=InviteRead)
def create_invite_endpoint(
    payload: InviteCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if payload.scope == "org":
        if not payload.organization_id:
            raise HTTPException(status_code=400, detail="organization_id is required for org invite.")
        invite = create_invite_for_org(
            session=session,
            email=payload.email,
            org_id=payload.organization_id or 0,
            role=payload.role,
            inviter_id=current_user.id,
            expires_in_hours=payload.expires_in_hours or 72,
        )
    elif payload.scope == "trip":
        if not payload.trip_id:
            raise HTTPException(status_code=400, detail="trip_id is required for trip invite.")
        invite = create_invite_for_trip(
            session=session,
            email=payload.email,
            trip_id=payload.trip_id or 0,
            role=payload.role,
            inviter_id=current_user.id,
            expires_in_hours=payload.expires_in_hours or 72,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid invite scope.")

    return InviteRead(**invite.model_dump())


@router.get("/{token}", response_model=InviteRead)
def get_invite_endpoint(token: str, session: Session = Depends(get_session)):
    invite = get_invite_by_token(session, token)
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found.")
    return InviteRead(**invite.model_dump())


@router.post("/accept", response_model=InviteRead)
def accept_invite_endpoint(
    payload: InviteAcceptRequest,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    invite = accept_invite(session, payload.token, current_user.id, current_user.email)
    return InviteRead(**invite.model_dump())
