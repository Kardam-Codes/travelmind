from typing import List, Optional

from sqlmodel import Session, select

from app.database.models.org_member import OrgMember


def create_org_member(session: Session, member: OrgMember) -> OrgMember:
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def get_org_member(session: Session, org_id: int, user_id: int) -> Optional[OrgMember]:
    statement = select(OrgMember).where(OrgMember.organization_id == org_id, OrgMember.user_id == user_id)
    return session.exec(statement).first()


def list_org_members(session: Session, org_id: int) -> List[OrgMember]:
    statement = select(OrgMember).where(OrgMember.organization_id == org_id).order_by(OrgMember.id.asc())
    return list(session.exec(statement).all())


def list_orgs_for_user(session: Session, user_id: int) -> List[OrgMember]:
    statement = select(OrgMember).where(OrgMember.user_id == user_id).order_by(OrgMember.id.asc())
    return list(session.exec(statement).all())


def update_org_member(session: Session, member: OrgMember) -> OrgMember:
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def delete_org_member(session: Session, member: OrgMember) -> None:
    session.delete(member)
    session.commit()
