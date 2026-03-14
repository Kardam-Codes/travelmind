"""
Feature: Auth Schemas
File Purpose: Request and response models for authentication APIs
Owner: Misha
Dependencies: sqlmodel
Last Updated: 2026-03-14
"""

from typing import Optional

from sqlmodel import SQLModel


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
