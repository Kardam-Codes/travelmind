
# Service Communication Contract

This document defines communication between:

Frontend → Backend → AI Service

---

# 1. Frontend → Backend APIs

## Generate Trip

POST /api/trip/generate

Request:

{
  "query": "Plan a 3 day Goa trip under 20k"
}

Response:

{
  "destination": "Goa",
  "duration": 3,
  "budget": 20000,
  "itinerary": [...]
}

---

## Save Wishlist

POST /api/wishlist

Request

{
  "item_id": "hotel_101"
}

---

## Fetch Recommendations

GET /api/recommendations?location=goa

Response

{
  "hotels": [...],
  "activities": [...]
}

---

# 2. Backend → AI Service

Base URL

http://localhost:8000

---

## Parse Intent

POST /ai/parse-intent

Request

{
  "query": "3 day Goa trip under 20k"
}

Response

{
  "destination": "Goa",
  "duration": 3,
  "budget": 20000
}

---

## Generate Itinerary

POST /ai/generate-itinerary

Request

{
  "destination": "Goa",
  "duration": 3,
  "preferences": ["beaches", "nightlife"]
}

Response

{
  "itinerary": [...]
}

---

# 3. Backend → Google Maps

## Route Optimization

POST /maps/optimize-route

Request

{
  "locations": ["Hotel", "Beach", "Market"]
}

Response

{
  "optimized_route": [...]
}

---

# 4. Real-Time Collaboration

Socket.io Events

JOIN_TRIP

UPDATE_ITINERARY

VOTE_ACTIVITY

SYNC_STATE
