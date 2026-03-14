from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.security import get_current_user_id
from app.database.session import get_session
from app.features.orgs.service import (
    add_member,
    create_org_with_owner,
    ensure_org_admin,
    ensure_org_member,
    get_org,
    list_members,
    list_user_orgs,
    remove_member,
    update_member_role,
)
from app.schemas.org import OrganizationCreate, OrganizationRead, OrganizationUpdate, OrgMemberCreate, OrgMemberRead, OrgMemberUpdate
from app.repositories.organization_repository import update_organization


router = APIRouter(prefix="/orgs", tags=["Organizations"])


@router.post("/", response_model=OrganizationRead)
def create_org_endpoint(
    payload: OrganizationCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    org = create_org_with_owner(session, payload.name, user_id)
    return OrganizationRead(id=org.id, name=org.name, slug=org.slug)


@router.get("/", response_model=list[OrganizationRead])
def list_orgs_endpoint(session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    memberships = list_user_orgs(session, user_id)
    orgs = [get_org(session, membership.organization_id) for membership in memberships]
    return [OrganizationRead(id=org.id, name=org.name, slug=org.slug) for org in orgs]


@router.get("/{org_id}", response_model=OrganizationRead)
def get_org_endpoint(
    org_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_member(session, org_id, user_id)
    org = get_org(session, org_id)
    return OrganizationRead(id=org.id, name=org.name, slug=org.slug)


@router.patch("/{org_id}", response_model=OrganizationRead)
def update_org_endpoint(
    org_id: int,
    payload: OrganizationUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_admin(session, org_id, user_id)
    org = get_org(session, org_id)
    if payload.name:
        org.name = payload.name
        org = update_organization(session, org)
    return OrganizationRead(id=org.id, name=org.name, slug=org.slug)


@router.get("/{org_id}/members", response_model=list[OrgMemberRead])
def list_members_endpoint(
    org_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_member(session, org_id, user_id)
    members = list_members(session, org_id)
    return [
        OrgMemberRead(id=member.id, organization_id=member.organization_id, user_id=member.user_id, role=member.role)
        for member in members
    ]


@router.post("/{org_id}/members", response_model=OrgMemberRead)
def add_member_endpoint(
    org_id: int,
    payload: OrgMemberCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_admin(session, org_id, user_id)
    member = add_member(session, org_id, payload.user_id, payload.role)
    return OrgMemberRead(id=member.id, organization_id=member.organization_id, user_id=member.user_id, role=member.role)


@router.patch("/{org_id}/members/{member_user_id}", response_model=OrgMemberRead)
def update_member_endpoint(
    org_id: int,
    member_user_id: int,
    payload: OrgMemberUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_admin(session, org_id, user_id)
    member = update_member_role(session, org_id, member_user_id, payload.role)
    return OrgMemberRead(id=member.id, organization_id=member.organization_id, user_id=member.user_id, role=member.role)


@router.delete("/{org_id}/members/{member_user_id}", status_code=204)
def remove_member_endpoint(
    org_id: int,
    member_user_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    ensure_org_admin(session, org_id, user_id)
    remove_member(session, org_id, member_user_id)
    return None
