import re
from typing import List

from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.organization import Organization
from app.database.models.org_member import OrgMember
from app.repositories.organization_repository import (
    create_organization,
    get_organization_by_id,
    get_organization_by_slug,
)
from app.repositories.org_member_repository import (
    create_org_member,
    get_org_member,
    list_org_members,
    list_orgs_for_user,
    update_org_member,
    delete_org_member,
)


ORG_ADMIN_ROLES = {"owner", "admin"}


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "organization"


def create_org_with_owner(session: Session, name: str, owner_user_id: int) -> Organization:
    slug = _slugify(name)
    existing = get_organization_by_slug(session, slug)
    if existing:
        slug = f"{slug}-{owner_user_id}"
    org = create_organization(session, Organization(name=name, slug=slug))
    create_org_member(
        session,
        OrgMember(organization_id=org.id, user_id=owner_user_id, role="owner"),
    )
    return org


def ensure_org_member(session: Session, org_id: int, user_id: int) -> OrgMember:
    member = get_org_member(session, org_id, user_id)
    if not member:
        raise HTTPException(status_code=403, detail="User does not belong to this organization.")
    return member


def ensure_org_admin(session: Session, org_id: int, user_id: int) -> OrgMember:
    member = ensure_org_member(session, org_id, user_id)
    if member.role not in ORG_ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Org admin privileges required.")
    return member


def list_user_orgs(session: Session, user_id: int) -> List[OrgMember]:
    return list_orgs_for_user(session, user_id)


def list_members(session: Session, org_id: int) -> List[OrgMember]:
    return list_org_members(session, org_id)


def add_member(session: Session, org_id: int, user_id: int, role: str) -> OrgMember:
    existing = get_org_member(session, org_id, user_id)
    if existing:
        existing.role = role
        return update_org_member(session, existing)
    return create_org_member(session, OrgMember(organization_id=org_id, user_id=user_id, role=role))


def update_member_role(session: Session, org_id: int, user_id: int, role: str) -> OrgMember:
    member = get_org_member(session, org_id, user_id)
    if not member:
        raise HTTPException(status_code=404, detail="Org member not found.")
    member.role = role
    return update_org_member(session, member)


def remove_member(session: Session, org_id: int, user_id: int) -> None:
    member = get_org_member(session, org_id, user_id)
    if not member:
        raise HTTPException(status_code=404, detail="Org member not found.")
    delete_org_member(session, member)


def get_org(session: Session, org_id: int) -> Organization:
    org = get_organization_by_id(session, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found.")
    return org
