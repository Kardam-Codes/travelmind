"""
Feature: User Model
File Purpose: Store application users for login and signup
Owner: Misha
Dependencies: sqlmodel
Last Updated: 2026-03-14
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    auth_provider: str = Field(default="local", nullable=False)
