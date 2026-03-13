# API Specification

## Base URL

/api

---

## Generate Trip

POST /trip/generate

### Request

{
  "query": "3 day Goa trip under 20k"
}

### Response

{
  "destination": "Goa",
  "duration": 3,
  "budget": 20000,
  "itinerary": [
    {
      "day": 1,
      "activities": ["Beach Walk", "Local Market"]
    },
    {
      "day": 2,
      "activities": ["Water Sports", "Sunset Point"]
    }
  ]
}

---

## Wishlist

POST /wishlist/add

### Request

{
  "item_id": "place_102"
}

### Response

{
  "status": "added"
}

---

## Collaboration

POST /collaboration/invite

### Request

{
  "trip_id": "123",
  "user_email": "friend@email.com"
}

### Response

{
  "status": "invited"
}

---

## Route Optimization

GET /route/optimize

### Request

{
  "locations": ["Beach", "Market", "Hotel"]
}

### Response

{
  "optimized_route": ["Hotel", "Beach", "Market"]
}