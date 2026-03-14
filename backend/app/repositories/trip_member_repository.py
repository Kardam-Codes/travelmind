from typing import List, Optional

from sqlmodel import Session, select

from app.database.models.trip_member import TripMember


def create_trip_member(session: Session, member: TripMember) -> TripMember:
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def get_trip_member(session: Session, trip_id: int, user_id: int) -> Optional[TripMember]:
    statement = select(TripMember).where(TripMember.trip_id == trip_id, TripMember.user_id == user_id)
    return session.exec(statement).first()


def list_trip_members(session: Session, trip_id: int) -> List[TripMember]:
    statement = select(TripMember).where(TripMember.trip_id == trip_id).order_by(TripMember.id.asc())
    return list(session.exec(statement).all())


def update_trip_member(session: Session, member: TripMember) -> TripMember:
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def delete_trip_member(session: Session, member: TripMember) -> None:
    session.delete(member)
    session.commit()
