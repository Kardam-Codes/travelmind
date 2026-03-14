from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.wishlist import WishlistItem
from app.repositories.wishlist_repository import (
    create_wishlist_item,
    delete_wishlist_item,
    get_wishlist_by_user_id,
)


def add_to_wishlist(session: Session, user_id: str, item_id: int, item_type: str) -> WishlistItem:
    wishlist_item = WishlistItem(user_id=user_id, item_id=item_id, item_type=item_type)
    return create_wishlist_item(session, wishlist_item)


def fetch_user_wishlist(session: Session, user_id: str):
    return get_wishlist_by_user_id(session, user_id)


def remove_from_wishlist(session: Session, wishlist_id: int):
    deleted = delete_wishlist_item(session, wishlist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Wishlist item not found.")

    return {"message": "Wishlist item removed successfully."}
