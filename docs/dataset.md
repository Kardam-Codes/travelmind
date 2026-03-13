"""
Feature: Dataset
File Purpose: Locked dataset schema, vocabularies, and validation rules
Owner: Kardam
Dependencies: datasets/city_master_list.csv, datasets/places.csv, datasets/activities.csv, datasets/hotels.csv
Last Updated: 2026-03-14
"""

# TravelMind Dataset Specification

## Purpose

TravelMind uses curated travel catalog data instead of letting the AI invent places,
activities, or hotels. The dataset acts as the source of truth for recommendation and
itinerary generation.

## Scope

- India only
- Manual curated data first
- Places are the anchor dataset
- Recommendations are city-first with distance-aware ranking

## Approved Core Files

- `datasets/city_master_list.csv`
- `datasets/places.csv`
- `datasets/activities.csv`
- `datasets/hotels.csv`
- `datasets/wishlist.csv` optional

## Locked Schemas

### `places.csv`

| Field | Type | Description |
|------|------|-------------|
| id | string/integer | unique place id |
| name | string | tourist place or landmark name |
| city | string | approved city name from master list |
| state | string | state matching approved city |
| category | enum | place category |
| tags | string | comma-separated descriptive tags |
| rating | float | rating on a 1 to 5 scale |
| price_estimate | number | estimated entry or visit cost |
| duration_hours | float | practical visit duration |
| latitude | float | latitude coordinate |
| longitude | float | longitude coordinate |
| popularity_score | integer | normalized popularity score, recommended 1 to 100 |
| best_time | string | best season or visit window |
| family_friendly | boolean | family suitability |
| foreign_tourist_friendly | boolean | fit for international travelers |

### `activities.csv`

| Field | Type | Description |
|------|------|-------------|
| id | string/integer | unique activity id |
| name | string | activity name |
| city | string | approved city name |
| state | string | state matching approved city |
| category | enum | activity category |
| tags | string | comma-separated descriptive tags |
| price | number | estimated cost |
| duration_hours | float | practical activity duration |
| rating | float | rating on a 1 to 5 scale |
| latitude | float | latitude coordinate |
| longitude | float | longitude coordinate |
| linked_place_id | string/integer | related place id when available |
| near_place_name | string | nearby place or area reference |
| popularity_score | integer | normalized popularity score, recommended 1 to 100 |

### `hotels.csv`

| Field | Type | Description |
|------|------|-------------|
| id | string/integer | unique hotel id |
| name | string | hotel name |
| city | string | approved city name |
| state | string | state matching approved city |
| price_per_night | number | average nightly rate |
| hotel_type | enum | hotel class/type |
| rating | float | rating on a 1 to 5 scale |
| latitude | float | latitude coordinate |
| longitude | float | longitude coordinate |
| budget_category | enum | budget band |
| nearby_area | string | locality or cluster name |
| popularity_score | integer | normalized popularity score, recommended 1 to 100 |

### `wishlist.csv`

| Field | Type | Description |
|------|------|-------------|
| user_id | string/integer | user identifier |
| item_id | string/integer | saved record id |
| item_type | enum | place, activity, or hotel |

## Controlled Vocabularies

### Place Categories

- beach
- lake
- fort
- palace
- temple
- museum
- market
- viewpoint
- nature
- heritage

### Activity Categories

- adventure
- cultural
- food
- entertainment
- wellness
- shopping
- sightseeing

### Hotel Types

- budget
- standard
- premium
- luxury
- hostel
- resort
- boutique

### Budget Categories

- low
- moderate
- high
- premium

### Traveler-Fit Tags

- family
- friends
- solo
- couple
- luxury
- backpacker
- spiritual
- adventure
- food
- heritage

## Recommendation Model

TravelMind uses a **city-first + radius assist** model.

### How it works

1. AI extracts destination, duration, budget, preferences, and traveler type
2. Backend pulls only records from the destination city as the primary candidate pool
3. Candidate places are ranked using:
   - category match
   - tag match
   - popularity
   - rating
   - practical travel distance
4. Activities are then selected around shortlisted places or place clusters
5. Hotels are ranked around the city center or dominant itinerary cluster
6. Google Maps data is used later to optimize route order

### Why not use a single fixed radius

- cities are not evenly shaped
- tourist demand appears in clusters, not perfect circles
- longer trips should expand coverage, not just distance
- fixed large radii can include low-value results and increase travel time

## Progressive Coverage by Duration

- 1 to 2 days: compact, high-value cluster
- 3 to 4 days: two or three clusters within the city or nearby zones
- 5 or more days: broader city coverage and practical nearby excursion options

### Example: Udaipur for 5 days

Interpretation:

- destination: Udaipur
- duration: 5
- budget: user defined or optional
- preferences: lakes, heritage, food

Recommended retrieval logic:

1. fetch Udaipur places only
2. prioritize categories such as `lake`, `palace`, `heritage`, `market`
3. group shortlisted places into clusters such as:
   - old city and palace zone
   - lake and sunset zone
   - culture or day-experience zone
4. assign more clusters because trip duration is longer
5. fetch nearby activities for each selected cluster
6. rank hotels around the most central or most-used cluster
7. pass final locations into route optimization

## Validation Rules

Every new row should satisfy the following checks:

- city exists in `city_master_list.csv`
- state matches the city-state mapping
- category belongs to the approved enum
- coordinates are present and plausible
- ratings are within a 1 to 5 scale
- prices are non-negative and realistic
- duration is practical for a traveler
- duplicates are reviewed before approval
- activities and hotels belong to approved cities only

## Population Sequence

1. approve city master list
2. populate places
3. populate activities
4. populate hotels
5. validate all rows
6. update docs if schema changes
