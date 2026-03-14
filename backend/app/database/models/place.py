"""
Feature: Place Model
File Purpose: Store city-scoped tourist places used for recommendations
Owner: Misha
Dependencies: sqlmodel
Last Updated: 2026-03-14
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    city: str = Field(nullable=False, index=True)
    state: str = Field(nullable=False)
    category: str = Field(nullable=False, index=True)
    tags: Optional[str] = None
    rating: Optional[float] = None
    price_estimate: Optional[float] = None
    duration_hours: Optional[float] = None
    latitude: float
    longitude: float
    popularity_score: Optional[int] = None
    best_time: Optional[str] = None
    family_friendly: bool = False
    foreign_tourist_friendly: bool = False
