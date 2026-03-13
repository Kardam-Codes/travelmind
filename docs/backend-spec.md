
# Backend Specification

## Overview

The backend is implemented using **FastAPI** and combines both backend API logic and AI services.

Responsibilities:

- Handle frontend API requests
- Perform intent extraction
- Generate travel itineraries
- Query travel catalog database
- Manage WebSocket collaboration
- Integrate Google Maps route optimization

---

# System Architecture

Frontend → FastAPI Backend → PostgreSQL / Google Maps API

The backend also provides WebSocket endpoints for real-time collaboration.

---

# AI Processing Flow

1. User submits natural language trip request
2. LLM extracts trip parameters:
   - destination
   - duration
   - budget
   - preferences
3. Python recommendation engine filters catalog data
4. Itinerary generator builds structured travel plan
5. Route optimization organizes travel order

---

# REST API Endpoints

## Generate Trip

POST /api/trip/generate

Request

{
  "query": "Plan a 3 day Goa trip under 20000"
}

Response

{
  "destination": "Goa",
  "duration": 3,
  "budget": 20000,
  "itinerary": [...]
}

---

## Recommendations

GET /api/recommendations?location=goa

Response

{
  "hotels": [...],
  "activities": [...]
}

---

## Wishlist

POST /api/wishlist/add

Request

{
  "item_id": "activity_101"
}

---

# WebSocket Collaboration

Endpoint:

/ws/trip/{trip_id}

Supported Events:

JOIN_TRIP

UPDATE_ITINERARY

VOTE_ACTIVITY

SYNC_STATE

Example Message

{
  "event": "UPDATE_ITINERARY",
  "data": {...}
}

---

# Database Schema

## Places

id
name
location
category
rating

## Hotels

id
name
location
price
rating

## Activities

id
name
location
category
price

---

# Route Optimization

Uses **Google Maps Distance Matrix API**

Steps:

1. Collect itinerary locations
2. Calculate travel distances
3. Optimize order to minimize travel time
4. Update itinerary schedule
