"""
Feature: Auth Schemas
File Purpose: Request and response models for authentication APIs
Owner: Misha
Dependencies: sqlmodel
Last Updated: 2026-03-14
"""

from typing import List, Optional

from sqlmodel import SQLModel

from app.schemas.org import OrganizationRead


class SignUpRequest(SQLModel):
    email: str
    password: str
    name: Optional[str] = None


class LoginRequest(SQLModel):
    email: str
    password: str


class GoogleAuthRequest(SQLModel):
    email: str
    name: Optional[str] = None


class AuthResponse(SQLModel):
    message: str
    user_id: int
    email: str
    access_token: str
    token_type: str = "bearer"
    organizations: List[OrganizationRead] = []
    default_org_id: Optional[int] = None


class UserRead(SQLModel):
    id: int
    name: Optional[str] = None
    email: str


class MeResponse(SQLModel):
    user: UserRead
    organizations: List[OrganizationRead] = []
    active_org_id: Optional[int] = None
