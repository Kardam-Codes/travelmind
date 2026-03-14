# Backend Specification

## Overview

The backend is implemented using FastAPI and keeps PostgreSQL as the source of truth for travel inventory, trips, itinerary state, and collaboration events.

Responsibilities:

- Handle frontend API requests
- Call the local AI service for trip intent extraction
- Validate extracted intent against supported cities and known tags
- Generate recommendations and itineraries from PostgreSQL-backed data
- Manage WebSocket collaboration with versioned itinerary edits

---

# System Architecture

Frontend -> FastAPI Backend -> PostgreSQL
Frontend -> FastAPI Backend -> Local AI Service

The backend also provides WebSocket endpoints for real-time collaboration.

---

# AI Processing Flow

1. User submits natural language trip request
2. Backend calls the AI service for structured intent extraction
3. Backend validates or requests clarification
4. Recommendation engine filters catalog data
5. Itinerary generator builds a structured travel plan

---

# Collaboration Flow

1. Client loads the canonical dashboard through REST
2. Client connects to `/ws/trip/{trip_id}?user_id={user_id}`
3. Client sends versioned itinerary operations
4. Server validates version and lock state
5. Server applies accepted changes in PostgreSQL and broadcasts canonical results

---

# Current Collaboration Events

- CHAT_MESSAGE
- ADD_ITEM
- REMOVE_ITEM
- MOVE_ITEM
- UPDATE_ITEM
- REORDER_DAY
- LOCK_DAY
- UNLOCK_DAY
- ITINERARY_APPLIED
- ITINERARY_REJECTED
- DAY_LOCK_CHANGED
- USER_PRESENCE
