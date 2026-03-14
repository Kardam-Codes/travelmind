"""
Feature: Database Session
File Purpose: Create database engine and session dependency
Owner: Misha
Dependencies: app/core/config.py
Last Updated: 2026-03-14
"""

from sqlmodel import Session, create_engine

from app.core.config import settings


engine = create_engine(settings.database_url, echo=settings.debug)


def get_session():
    with Session(engine) as session:
        yield session
