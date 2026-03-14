from typing import List, Optional

from sqlmodel import Session, select

from app.database.models.organization import Organization


def create_organization(session: Session, org: Organization) -> Organization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


def get_organization_by_id(session: Session, org_id: int) -> Optional[Organization]:
    statement = select(Organization).where(Organization.id == org_id)
    return session.exec(statement).first()


def get_organization_by_slug(session: Session, slug: str) -> Optional[Organization]:
    statement = select(Organization).where(Organization.slug == slug)
    return session.exec(statement).first()


def list_organizations(session: Session) -> List[Organization]:
    statement = select(Organization).order_by(Organization.name.asc())
    return list(session.exec(statement).all())


def update_organization(session: Session, org: Organization) -> Organization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org
