from typing import List
from sqlmodel import Session, select
from app.database.models.wishlist import WishlistItem


def create_wishlist_item(session: Session, wishlist_item: WishlistItem) -> WishlistItem:
    session.add(wishlist_item)
    session.commit()
    session.refresh(wishlist_item)
    return wishlist_item


def get_wishlist_by_user_id(session: Session, user_id: str) -> List[WishlistItem]:
    statement = select(WishlistItem).where(WishlistItem.user_id == user_id)
    return list(session.exec(statement).all())


def delete_wishlist_item(session: Session, wishlist_id: int) -> bool:
    wishlist_item = session.get(WishlistItem, wishlist_id)
    if not wishlist_item:
        return False

    session.delete(wishlist_item)
    session.commit()
    return True
