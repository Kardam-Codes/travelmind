from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OrgMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(nullable=False, index=True, foreign_key="organization.id")
    user_id: int = Field(nullable=False, index=True, foreign_key="user.id")
    role: str = Field(nullable=False, default="member", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
