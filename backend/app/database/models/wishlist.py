from typing import Optional
from sqlmodel import Field, SQLModel


class WishlistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, index=True)
    item_id: int = Field(nullable=False, index=True)
    item_type: str = Field(nullable=False, index=True)
