from typing import Optional
from sqlmodel import SQLModel


class OrganizationCreate(SQLModel):
    name: str


class OrganizationUpdate(SQLModel):
    name: Optional[str] = None


class OrganizationRead(SQLModel):
    id: int
    name: str
    slug: str


class OrgMemberCreate(SQLModel):
    user_id: int
    role: str = "member"


class OrgMemberUpdate(SQLModel):
    role: str


class OrgMemberRead(SQLModel):
    id: int
    organization_id: int
    user_id: int
    role: str
