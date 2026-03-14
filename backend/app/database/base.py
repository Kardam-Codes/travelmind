"""
Feature: Database Base
File Purpose: Provide a shared SQLModel base import for models and table creation
Owner: Misha
Dependencies: sqlmodel, app/database/session.py
Last Updated: 2026-03-14
"""

from sqlmodel import SQLModel

from app.database.session import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
