"""
Feature: User Repository
File Purpose: Database queries for user authentication records
Owner: Misha
Dependencies: app/database/models/user.py
Last Updated: 2026-03-14
"""

from typing import Optional

from sqlmodel import Session, select

from app.database.models.user import User


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
