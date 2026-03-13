"""
Feature: AI Context
File Purpose: Dataset and recommendation guidance for Yug's AI implementation
Owner: Kardam
Dependencies: docs/dataset.md, docs/dataset-usage-contract.md, datasets/city_master_list.csv, datasets/places.csv, datasets/activities.csv, datasets/hotels.csv
Last Updated: 2026-03-14
"""

# Yug Context

## How To Use This Context

Use this file as the working reference while building:

- intent extraction outputs
- recommendation engine logic
- itinerary generation logic

Read this before writing code so your AI layer stays aligned with the dataset structure.
Do not invent fields, categories, or city names outside the approved dataset files.
If implementation and this context ever conflict, prefer the dataset contract and schema docs.

## Your Role In TravelMind

Yug owns:

- AI logic
- intent extraction
- recommendation engine
- itinerary generation algorithm

Your work should convert user intent into ranked, realistic travel options using the
curated dataset. The AI should not hallucinate places, hotels, or activities that do not
exist in the dataset.

## Dataset Source Of Truth

Use these files as the source of truth:

- `datasets/city_master_list.csv`
- `datasets/places.csv`
- `datasets/activities.csv`
- `datasets/hotels.csv`

Supporting references:

- `docs/dataset.md`
- `docs/dataset-usage-contract.md`

## Core Product Rule

TravelMind uses a **city-first + radius assist** recommendation model.

This means:

1. extract destination city from the user query
2. validate it against `city_master_list.csv`
3. fetch only that city's records as the primary pool
4. rank and cluster places using preference fit and geographic practicality
5. attach nearby activities and hotels after places are shortlisted

Do not start by searching across all cities once destination is known.

## What Intent Extraction Should Produce

At minimum, your parser should try to derive:

- `destination_city`
- `duration_days`
- `budget_total`
- `preferences`
- `traveler_type`

Optional enrichments if clear from query:

- trip style
- hotel comfort level
- must-have attraction type
- pace preference such as relaxed or packed

## Recommendation Retrieval Logic

### Step 1: City Validation

- match destination against `city_master_list.csv`
- reject or normalize unsupported city names
- keep `Goa` as a valid anchor destination

### Step 2: Place Selection First

Places are the anchor dataset.

Start with `places.csv` and score candidates using:

- category match
- tag match
- popularity score
- rating
- family suitability
- foreign tourist suitability
- estimated visit duration
- geographic practicality

### Step 3: Progressive Coverage

Do not use one fixed radius for all trip lengths.

Use trip duration like this:

- 1 to 2 days: one compact cluster
- 3 to 4 days: two or three clusters
- 5 or more days: broader city coverage plus practical nearby options

### Step 4: Add Activities

After place selection:

- fetch activities near selected places or clusters
- use `linked_place_id` when available
- otherwise use `near_place_name`, coordinates, and city match

Score activities using:

- category fit
- tag fit
- price fit
- rating
- duration fit
- proximity to selected places

### Step 5: Add Hotels

Hotels should be selected after the likely itinerary shape is known.

Rank hotels using:

- budget fit
- price per night
- rating
- popularity score
- nearby area relevance
- centrality to major place clusters

## Why This Model Matters

A strict single-radius-only approach is weak because:

- cities are not perfect circles
- tourist attractions appear in clusters
- longer trips should expand practical coverage, not just distance
- a large radius can add low-value places with poor travel efficiency

## Example Query

User query:

`Plan a 5 day Udaipur trip under 25000 with lakes, heritage, and good food`

Expected AI flow:

1. extract `Udaipur`, `5`, `25000`, `lakes`, `heritage`, `food`
2. fetch only Udaipur places
3. prioritize categories like `lake`, `palace`, `heritage`, `market`
4. build clusters such as:
   - old city and palace zone
   - lake and sunset zone
   - culture or local experience zone
5. choose enough places for 5 days without overloading travel
6. attach nearby activities
7. pass shortlisted hotels and coordinates to itinerary planning

## Important Dataset Constraints

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

## Validation Expectations For AI Use

Before using a record:

- city must be approved
- state must match city
- category must be valid
- coordinates must exist
- prices must be non-negative
- rating must be within the expected scale

If data is missing or weak, degrade gracefully by lowering rank instead of inventing values.

## Output Expected From Your Layer

Your recommendation or itinerary preparation layer should output:

- ranked places
- relevant activities
- hotel candidates
- route-ready coordinates
- enough metadata for downstream itinerary generation

Do not return an unfiltered city-wide dump as the final recommendation set.
