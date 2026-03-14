from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.wishlist import WishlistItem
from app.repositories.activity_repository import get_activity_by_id
from app.repositories.hotel_repository import get_hotel_by_id
from app.repositories.place_repository import get_place_by_id
from app.repositories.wishlist_repository import (
    create_wishlist_item,
    delete_wishlist_item,
    get_wishlist_by_user_id,
)


def add_to_wishlist(session: Session, user_id: str, item_id: int, item_type: str) -> WishlistItem:
    wishlist_item = WishlistItem(user_id=user_id, item_id=item_id, item_type=item_type)
    return create_wishlist_item(session, wishlist_item)


def fetch_user_wishlist(session: Session, user_id: str):
    items = get_wishlist_by_user_id(session, user_id)
    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "item_id": item.item_id,
            "item_type": item.item_type,
            "item_name": _resolve_item_name(session, item.item_type, item.item_id),
        }
        for item in items
    ]


def remove_from_wishlist(session: Session, wishlist_id: int):
    deleted = delete_wishlist_item(session, wishlist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Wishlist item not found.")

    return {"message": "Wishlist item removed successfully."}


def _resolve_item_name(session: Session, item_type: str, item_id: int) -> str:
    if item_type == "place":
        item = get_place_by_id(session, item_id)
    elif item_type == "hotel":
        item = get_hotel_by_id(session, item_id)
    elif item_type == "activity":
        item = get_activity_by_id(session, item_id)
    else:
        item = None

    return item.name if item else f"{item_type.title()} #{item_id}"
