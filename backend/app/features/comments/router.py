from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.security import get_current_org_id, get_current_user
from app.database.session import get_session
from app.features.comments.service import add_comment, list_trip_comments
from app.repositories.comment_repository import get_comment_by_id, delete_comment
from app.features.trips.permissions import ensure_org_member, ensure_trip_member_role, ensure_trip_owner_or_admin
from app.schemas.comment import CommentCreate, CommentRead


router = APIRouter(prefix="/trips", tags=["Comments"])


@router.get("/{trip_id}/comments", response_model=list[CommentRead])
def list_comments_endpoint(
    trip_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, current_user.id)
    ensure_trip_member_role(session, trip_id, current_user.id, minimum_role="viewer")
    comments = list_trip_comments(session, trip_id)
    return [CommentRead(**comment.model_dump()) for comment in comments]


@router.post("/{trip_id}/comments", response_model=CommentRead)
def add_comment_endpoint(
    trip_id: int,
    payload: CommentCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, current_user.id)
    ensure_trip_member_role(session, trip_id, current_user.id, minimum_role="editor")
    comment = add_comment(session, trip_id, current_user.id, payload.body, payload.itinerary_item_id)
    return CommentRead(**comment.model_dump())


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment_endpoint(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    org_id: int = Depends(get_current_org_id),
):
    comment = get_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    ensure_org_member(session, org_id, current_user.id)
    ensure_trip_owner_or_admin(session, comment.trip_id, current_user.id)
    delete_comment(session, comment)
    return None
