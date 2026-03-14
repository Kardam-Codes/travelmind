"""
Feature: Collaboration Model
File Purpose: Store basic collaboration events and votes for shared trip planning
Owner: Misha
Dependencies: sqlmodel
Last Updated: 2026-03-14
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class CollaborationEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(nullable=False, index=True)
    user_id: str = Field(nullable=False, index=True)
    event_type: str = Field(nullable=False, index=True)
    payload: Optional[str] = None
