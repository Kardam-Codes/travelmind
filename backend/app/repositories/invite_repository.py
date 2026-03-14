from typing import Optional

from sqlmodel import Session, select

from app.database.models.invite import Invite


def create_invite(session: Session, invite: Invite) -> Invite:
    session.add(invite)
    session.commit()
    session.refresh(invite)
    return invite


def get_invite_by_token(session: Session, token: str) -> Optional[Invite]:
    statement = select(Invite).where(Invite.token == token)
    return session.exec(statement).first()


def update_invite(session: Session, invite: Invite) -> Invite:
    session.add(invite)
    session.commit()
    session.refresh(invite)
    return invite
