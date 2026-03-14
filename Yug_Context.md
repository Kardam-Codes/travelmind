"""
Feature: AI Context
File Purpose: Complete dataset and recommendation handoff for Yug's AI implementation
Owner: Kardam
Dependencies: docs/dataset.md, docs/dataset-usage-contract.md, datasets/city_master_list.csv, datasets/places.csv, datasets/activities.csv, datasets/hotels.csv
Last Updated: 2026-03-14
"""

# Yug Context

## How To Use This Context

Use this file as the source of truth before continuing AI work.

Read this in order:

1. `datasets/city_master_list.csv`
2. `datasets/places.csv`
3. `datasets/activities.csv`
4. `datasets/hotels.csv`
5. `docs/dataset.md`
6. `docs/dataset-usage-contract.md`

Use this context while building:

- intent extraction
- recommendation engine
- itinerary generation
- ranking logic

Do not invent destinations, categories, hotels, places, or activities outside the dataset.
If implementation ever conflicts with this file, prefer the dataset files and dataset docs.

## Current Dataset Status

This is the exact handoff point from Kardam.

### Completed

- `city_master_list.csv` completed for **54 approved destinations**
- `places.csv` completed for **all 54 destinations**
- `activities.csv` completed for **10 destinations**
- `hotels.csv` completed for **10 destinations**

### Counts

- `city_master_list.csv`: 54 rows
- `places.csv`: 320 rows
- `activities.csv`: 100 rows
- `hotels.csv`: 90 rows

### Cities With Full Place + Activity + Hotel Coverage

- Goa
- Jaipur
- Delhi
- Udaipur
- Manali
- Rishikesh
- Mumbai
- Varanasi
- Kochi
- Agra

### Cities With Places Complete But Activities And Hotels Pending

- Jodhpur
- Pushkar
- Amritsar
- Mysuru
- Shimla
- Darjeeling
- Puducherry
- Hampi
- Srinagar
- Jaisalmer
- Leh
- Chennai
- Bengaluru
- Alappuzha
- Ahmedabad
- Dwarka
- Somnath
- Madurai
- Ooty
- Kodaikanal
- Hyderabad
- Aurangabad
- Nashik
- Bhopal
- Khajuraho
- Gwalior
- Bhubaneswar
- Puri
- Konark
- Gangtok
- Shillong
- Tawang
- Port Blair
- Panaji
- Tirupati
- Varkala
- Mahabalipuram
- Mount Abu
- Ajmer
- Orchha
- McLeod Ganj
- Kanyakumari
- Ujjain
- Kozhikode

## Your Role In TravelMind

Yug owns:

- AI logic
- intent extraction
- recommendation engine
- itinerary generation algorithm

Your system should convert user intent into ranked and practical travel output using the
curated dataset only.

The AI should not hallucinate:

- unsupported cities
- missing places
- hotels not in the dataset
- activities not in the dataset

## Core Product Rule

TravelMind uses a **city-first + radius assist** recommendation model.

That means:

1. extract destination city from the query
2. validate city using `city_master_list.csv`
3. fetch only that city's places as the primary pool
4. cluster and rank those places
5. attach activities near shortlisted places when available
6. attach hotels near likely itinerary clusters when available

Do not start with all-India retrieval once destination is known.

## What Intent Extraction Should Produce

At minimum, your parser should derive:

- `destination_city`
- `duration_days`
- `budget_total`
- `preferences`
- `traveler_type`

Optional enrichments:

- pace preference
- trip style
- hotel comfort level
- must-have attraction type

## Dataset Source Of Truth

Primary files:

- `datasets/city_master_list.csv`
- `datasets/places.csv`
- `datasets/activities.csv`
- `datasets/hotels.csv`

Reference docs:

- `docs/dataset.md`
- `docs/dataset-usage-contract.md`

## Important Schema Notes

### `city_master_list.csv`

Contains:

- city
- state
- tier
- tourism_type
- latitude
- longitude
- best_season
- popularity_score
- notes

Use it for:

- city validation
- destination normalization
- city-level popularity weighting
- city center coordinates
- seasonal recommendation adjustments

### `places.csv`

This is the anchor dataset and is fully populated across all approved cities.

Key fields:

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

Currently available only for the first 10 cities listed above.

Key fields:

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

Currently available only for the first 10 cities listed above.

Key fields:

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

## Controlled Categories

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

## Recommendation Logic You Should Use

### Step 1: Validate City

- destination must match `city_master_list.csv`
- `Goa` stays valid as an anchor destination
- reject or normalize unsupported destination strings

### Step 2: Fetch Places First

Always start from `places.csv`.

Score places using:

- category match
- tag match
- popularity score
- rating
- visit duration fit
- city-level popularity
- season fit when relevant
- family suitability
- foreign tourist suitability
- travel practicality

### Step 3: Progressive Coverage By Trip Duration

Do not use one fixed radius.

Use this model:

- 1 to 2 days: one compact cluster
- 3 to 4 days: two or three clusters
- 5 or more days: broader city coverage plus practical nearby options

### Step 4: Attach Activities

If activities exist for the city:

- use `linked_place_id` first
- otherwise use `near_place_name`, coordinates, and city match

If activities do not exist for that city yet:

- degrade gracefully
- continue with place-led itinerary generation
- do not invent activities

### Step 5: Attach Hotels

If hotels exist for the city:

- rank by budget fit
- price per night
- rating
- popularity score
- nearby area relevance
- centrality to itinerary clusters

If hotels do not exist for that city yet:

- return place recommendations without fabricated hotel data

## Practical AI Behavior For Partial Dataset Coverage

This is important because place coverage is ahead of hotel/activity coverage.

### For cities with full place/activity/hotel data

Return:

- place shortlist
- activity shortlist
- hotel shortlist
- route-ready coordinates

### For cities with places only

Return:

- place shortlist
- cluster-aware itinerary candidate set
- explicit indication that supporting activity/hotel coverage is pending if needed internally

Do not fabricate missing support data just to fill UI space.

## Example Query

Query:

`Plan a 5 day Udaipur trip under 25000 with lakes, heritage, and good food`

Expected AI flow:

1. extract `Udaipur`, `5`, `25000`, `lakes`, `heritage`, `food`
2. fetch only Udaipur places
3. prioritize `lake`, `palace`, `heritage`, `market`
4. form clusters such as:
   - old city and palace zone
   - lake and sunset zone
   - cultural experience zone
5. attach activities because Udaipur has activity coverage
6. attach hotels because Udaipur has hotel coverage
7. pass ranked, route-ready output to itinerary logic

## Immediate Next Work For Yug

The strongest next AI work items are:

1. Build city validation and intent normalization against `city_master_list.csv`
2. Build place-ranking logic using `places.csv`
3. Support partial dataset fallback for cities missing activities/hotels
4. Build cluster-aware itinerary selection using place coordinates
5. Add season-aware and budget-aware ranking

## Validation Expectations

Before using a record:

- city must be approved
- state must match city
- category must be valid
- coordinates must exist
- prices must be non-negative
- rating must be in expected range

If data quality is weak for a candidate, lower its rank. Do not hallucinate replacement values.

## Output Expected From Your Layer

Your output should provide:

- ranked places
- relevant activities when available
- hotel candidates when available
- route-ready coordinates
- enough structure for itinerary generation

Do not return an unfiltered city-wide dump.
