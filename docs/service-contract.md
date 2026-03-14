# Service Communication Contract

This document defines communication between:

Frontend -> Backend -> AI Service

---

# 1. Frontend -> Backend APIs

## Generate Trip

POST /trips/generate-from-query

Request:

{
  "query": "Plan a 3 day Goa trip under 20k"
}

Response when ready:

{
  "status": "ready",
  "trip": {...},
  "places": [...],
  "activities": [...],
  "hotels": [...],
  "itinerary": {...},
  "ai_provider": "ollama-local"
}

Response when clarification is needed:

{
  "status": "clarification_needed",
  "missing_fields": ["destination_city"],
  "suggested_questions": ["Which supported city do you want to visit?"]
}

---

## Fetch Dashboard

GET /trips/{trip_id}/dashboard

Returns the canonical trip, recommendation, and itinerary state from PostgreSQL.

---

## Save Wishlist

POST /wishlist/

Request:

{
  "user_id": "12",
  "item_id": 101,
  "item_type": "place"
}

---

# 2. Backend -> AI Service

Base URL:

http://localhost:8001

---

## Extract Intent

POST /ai/extract-intent

Request:

{
  "query": "3 day Goa trip under 20k",
  "supported_cities": ["Goa", "Jaipur"],
  "allowed_preference_tags": ["beach", "food", "heritage"],
  "allowed_traveler_types": ["solo", "family", "couple", "friends"]
}

Response:

{
  "destination_city": "Goa",
  "duration_days": 3,
  "budget_total": 20000,
  "budget_level": "moderate",
  "preferences": ["beach"],
  "traveler_type": "friends",
  "confidence": 0.82,
  "missing_fields": [],
  "raw_reasoning_summary": "...",
  "normalized_query": "Plan a 3 day Goa trip under 20k",
  "provider": "ollama-local"
}

---

# 3. Real-Time Collaboration

WebSocket endpoint:

/ws/trip/{trip_id}?user_id={user_id}

Supported messages:

- CHAT_MESSAGE
- SYNC_SNAPSHOT
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
