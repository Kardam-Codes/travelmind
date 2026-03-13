"""
Feature: Dataset
File Purpose: Travel catalog dataset blueprint and usage notes
Owner: Kardam
Dependencies: places.csv, activities.csv, hotels.csv, wishlist.csv, city_master_list.csv
Last Updated: 2026-03-14
"""

# TravelMind Dataset Blueprint

This folder contains the structured travel catalog that powers TravelMind recommendations
and itinerary generation.

## Scope

- India only
- Manual curated data first
- City-first recommendation model with radius assist
- Places are the anchor dataset

## Files

- `city_master_list.csv`: approved Indian tourist cities grouped by tier with coordinates, best season, and city-level popularity score
- `places.csv`: tourist places and landmarks
- `activities.csv`: activities near places or city clusters
- `hotels.csv`: hotels mapped to city areas and budget levels
- `wishlist.csv`: optional user-saved items

## City Master List Fields

- `city`
- `state`
- `tier`
- `tourism_type`
- `latitude`
- `longitude`
- `best_season`
- `popularity_score`
- `notes`

Why these fields matter:

- coordinates support route-aware planning and future map features
- best season improves recommendation quality
- popularity score helps ranking cities before place-level scoring is applied

## Population Order

1. Finalize `city_master_list.csv`
2. Populate `places.csv`
3. Populate `activities.csv`
4. Populate `hotels.csv`
5. Run validation checks
6. Update documentation if schema or categories change

## Recommendation Model

TravelMind should not treat distance as one fixed circle around a city.

Recommended flow:

1. AI extracts destination, duration, budget, preferences, and traveler type
2. Backend filters records by destination city first
3. Places are ranked by category match, popularity, rating, and practical distance
4. Nearby activities are fetched around shortlisted places or clusters
5. Hotels are ranked around city center or selected place clusters
6. Route optimization arranges visits into a realistic itinerary

## Validation Rules

- city must exist in `city_master_list.csv`
- state must match the approved city-state mapping
- category values must use controlled vocabularies
- coordinates must be present and plausible
- prices must be realistic and non-negative
- duration values must be practical
- duplicate names must be reviewed before merge

## Notes

- Use finite categories and tags
- Keep coordinates for every place, activity, and hotel
- Prefer realistic values over volume during the hackathon
