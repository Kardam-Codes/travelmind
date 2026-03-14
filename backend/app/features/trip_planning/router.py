"""
Feature: Trip Planning Router
File Purpose: Expose API endpoints for creating and fetching trips
Owner: Misha
Dependencies: fastapi, app/api/deps.py, app/features/trip_planning/service.py, app/schemas/trip.py
Last Updated: 2026-03-14
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.session import get_session
from app.features.trip_planning.service import create_trip_plan, fetch_all_trips, fetch_trip
from app.schemas.trip import TripCreate, TripRead


router = APIRouter(prefix="/trips", tags=["Trip Planning"])


@router.post("/", response_model=TripRead)
def create_trip_endpoint(trip_data: TripCreate, session: Session = Depends(get_session)):
    return create_trip_plan(session, trip_data)


@router.get("/", response_model=List[TripRead])
def get_all_trips_endpoint(session: Session = Depends(get_session)):
    return fetch_all_trips(session)


@router.get("/{trip_id}", response_model=TripRead)
def get_trip_endpoint(trip_id: int, session: Session = Depends(get_session)):
    trip = fetch_trip(session, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    return trip
