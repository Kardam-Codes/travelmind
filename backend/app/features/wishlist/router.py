from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel

from app.database.session import get_session
from app.features.wishlist.service import add_to_wishlist, fetch_user_wishlist, remove_from_wishlist
from app.schemas.common import MessageResponse


class WishlistCreate(SQLModel):
    user_id: str
    item_id: int
    item_type: str


class WishlistRead(SQLModel):
    id: int
    user_id: str
    item_id: int
    item_type: str


router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/", response_model=WishlistRead)
def add_to_wishlist_endpoint(data: WishlistCreate, session: Session = Depends(get_session)):
    return add_to_wishlist(session, data.user_id, data.item_id, data.item_type)


@router.get("/{user_id}", response_model=List[WishlistRead])
def get_wishlist_endpoint(user_id: str, session: Session = Depends(get_session)):
    return fetch_user_wishlist(session, user_id)


@router.delete("/{wishlist_id}", response_model=MessageResponse)
def delete_wishlist_endpoint(wishlist_id: int, session: Session = Depends(get_session)):
    return remove_from_wishlist(session, wishlist_id)
