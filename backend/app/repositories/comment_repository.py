from typing import List, Optional

from sqlmodel import Session, select

from app.database.models.comment import Comment


def create_comment(session: Session, comment: Comment) -> Comment:
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def list_comments_for_trip(session: Session, trip_id: int) -> List[Comment]:
    statement = select(Comment).where(Comment.trip_id == trip_id).order_by(Comment.id.asc())
    return list(session.exec(statement).all())


def get_comment_by_id(session: Session, comment_id: int) -> Optional[Comment]:
    statement = select(Comment).where(Comment.id == comment_id)
    return session.exec(statement).first()


def delete_comment(session: Session, comment: Comment) -> None:
    session.delete(comment)
    session.commit()
