from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    slug: str = Field(nullable=False, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
