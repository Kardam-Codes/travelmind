"""
Feature: Dataset Contract
File Purpose: Define how backend and AI should consume the travel dataset
Owner: Kardam
Dependencies: docs/dataset.md, datasets/city_master_list.csv, datasets/places.csv, datasets/activities.csv, datasets/hotels.csv
Last Updated: 2026-03-14
"""

# Dataset Usage Contract

## Purpose

This document defines how the backend and AI layers should consume the TravelMind
dataset so recommendations and itineraries remain grounded in curated catalog data.

## Input Expected from AI Intent Extraction

The backend should receive or derive:

- `destination_city`
- `duration_days`
- `budget_total`
- `preferences`
- `traveler_type`

## Retrieval Order

1. Validate `destination_city` against `datasets/city_master_list.csv`
2. Filter `places.csv` by destination city
3. Rank places by preference fit, category fit, popularity, rating, and practical distance
4. Group shortlisted places into city clusters when useful
5. Fetch `activities.csv` records near selected places or clusters
6. Fetch `hotels.csv` records near city center or dominant clusters
7. Apply price and popularity ranking
8. Send final location set to route optimization

## Ranking Guidance

### Place Ranking Inputs

- category match
- tag match
- popularity score
- rating
- family or foreign traveler suitability
- estimated visit duration
- geographic practicality

### Activity Ranking Inputs

- near selected places
- category and tag match
- rating
- price fit
- duration fit

### Hotel Ranking Inputs

- price per night
- budget category
- nearby area relevance
- rating
- popularity score
- distance to major itinerary cluster

## Progressive Coverage Rule

The recommendation engine should expand coverage gradually:

- short trips favor one compact cluster
- medium trips allow multiple clusters inside the city
- longer trips allow broader coverage and practical nearby excursions

Duration should not be converted into one single large radius without clustering.

## Example Query

Query:

`Plan a 5 day Udaipur trip under 25000 with lakes, heritage, and good food`

Expected backend behavior:

1. filter records for Udaipur
2. rank places using categories like `lake`, `palace`, `heritage`, `market`
3. select a realistic number of places for 5 days
4. attach activities near chosen places
5. choose hotels matching budget and centrality
6. optimize the final route with maps

## Output Expectation

The itinerary generator should receive a curated, ranked set of:

- candidate places
- supporting activities
- hotel options
- route-ready coordinates

It should not receive unfiltered city-wide records as the final list.
