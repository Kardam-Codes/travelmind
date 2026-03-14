from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.comment import Comment
from app.repositories.comment_repository import create_comment, delete_comment, get_comment_by_id, list_comments_for_trip


def list_trip_comments(session: Session, trip_id: int):
    return list_comments_for_trip(session, trip_id)


def add_comment(session: Session, trip_id: int, author_id: int, body: str, itinerary_item_id: int | None = None):
    if not body.strip():
        raise HTTPException(status_code=400, detail="Comment body cannot be empty.")
    return create_comment(
        session,
        Comment(trip_id=trip_id, author_id=author_id, body=body.strip(), itinerary_item_id=itinerary_item_id),
    )


def remove_comment(session: Session, comment_id: int):
    comment = get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    delete_comment(session, comment)
    return comment
