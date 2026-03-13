"""
Feature: Backend Context
File Purpose: Dataset and retrieval guidance for Misha's backend implementation
Owner: Kardam
Dependencies: docs/dataset.md, docs/dataset-usage-contract.md, datasets/city_master_list.csv, datasets/places.csv, datasets/activities.csv, datasets/hotels.csv
Last Updated: 2026-03-14
"""

# Misha Context

## How To Use This Context

Use this file before building backend models, service logic, and API handlers that touch
travel data.

This context defines:

- which dataset files exist
- what schema they follow
- how data should be queried
- what order of filtering and ranking the backend should support

Do not design backend data access around assumptions that conflict with the dataset docs.
If something is unclear, align with `docs/dataset.md` and `docs/dataset-usage-contract.md`.

## Your Role In TravelMind

Misha owns:

- FastAPI backend development
- database models
- API endpoints

Your backend should expose data to the frontend and AI pipeline in a way that respects
the dataset contract and keeps recommendations grounded in curated records.

## Dataset Source Of Truth

Primary files:

- `datasets/city_master_list.csv`
- `datasets/places.csv`
- `datasets/activities.csv`
- `datasets/hotels.csv`
- `datasets/wishlist.csv` optional

Supporting references:

- `docs/dataset.md`
- `docs/dataset-usage-contract.md`

## Core Retrieval Rule

TravelMind uses a **city-first + radius assist** model.

Backend implication:

1. validate destination city
2. filter primary candidate records by city
3. support ranking inputs such as tags, category, rating, popularity, cost, and distance
4. support clustering or locality-based grouping where needed
5. support downstream route optimization with coordinates

The backend should not treat recommendations as a raw all-India search once a destination
is known.

## Expected Input From AI Layer

The backend should be prepared to consume:

- `destination_city`
- `duration_days`
- `budget_total`
- `preferences`
- `traveler_type`

These may come from an AI parsing layer or from request normalization logic.

## Dataset Schemas You Should Code Against

### `places.csv`

Fields:

- `id`
- `name`
- `city`
- `state`
- `category`
- `tags`
- `rating`
- `price_estimate`
- `duration_hours`
- `latitude`
- `longitude`
- `popularity_score`
- `best_time`
- `family_friendly`
- `foreign_tourist_friendly`

### `activities.csv`

Fields:

- `id`
- `name`
- `city`
- `state`
- `category`
- `tags`
- `price`
- `duration_hours`
- `rating`
- `latitude`
- `longitude`
- `linked_place_id`
- `near_place_name`
- `popularity_score`

### `hotels.csv`

Fields:

- `id`
- `name`
- `city`
- `state`
- `price_per_night`
- `hotel_type`
- `rating`
- `latitude`
- `longitude`
- `budget_category`
- `nearby_area`
- `popularity_score`

## Backend Querying Sequence

Recommended retrieval order:

1. validate `destination_city` against `city_master_list.csv`
2. query places for that city only
3. apply ranking and filtering for preference fit
4. group shortlisted places into practical clusters if needed
5. query activities linked to selected places or nearby areas
6. query hotels around central itinerary clusters or city center
7. pass final coordinate set to maps or route optimization

## Practical Filtering Guidance

### Place Filtering

Support filtering by:

- city
- category
- tags
- rating threshold
- popularity threshold
- family suitability
- foreign tourist suitability

### Activity Filtering

Support filtering by:

- city
- category
- price range
- linked place
- near place name
- duration fit

### Hotel Filtering

Support filtering by:

- city
- price per night
- budget category
- hotel type
- nearby area
- rating threshold

## Progressive Coverage Logic

Trip duration should influence how wide the plan spreads across the city.

Recommended support behavior:

- 1 to 2 days: compact local cluster
- 3 to 4 days: two or three clusters
- 5 or more days: broader coverage and practical nearby excursions

Do not encode this as one fixed large radius only.

## Example Backend Scenario

Query:

`Plan a 5 day Udaipur trip under 25000 with lakes, heritage, and good food`

Recommended backend flow:

1. normalize and validate `Udaipur`
2. fetch Udaipur places
3. prioritize `lake`, `palace`, `heritage`, `market` categories
4. return a ranked shortlist or cluster-aware candidate set
5. fetch nearby activities for shortlisted places
6. fetch hotels within budget near key clusters
7. send final location coordinates for route optimization

## Validation Rules The Backend Should Enforce

At minimum:

- city must exist in `city_master_list.csv`
- state must match approved mapping
- enum values must be valid
- coordinates must be present for route-aware features
- numeric values such as price, rating, duration, and popularity must be sane

If invalid records are encountered, reject them from recommendation output or flag them for review.

## API And Service Design Implications

Your service layer should make it easy to:

- fetch city-scoped places
- fetch activities near shortlisted places
- fetch hotels by area and budget
- return coordinates for maps
- support future ranking logic without changing schema

Keep the retrieval interface structured enough that Yug's AI layer can request ranked
candidate pools rather than raw unfiltered datasets.
