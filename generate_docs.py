import os
import subprocess

DOCS_DIR = "docs"

files = {

"architecture.md": """
# TravelMind System Architecture

## Overview

TravelMind is an AI-powered travel planning platform that converts natural language
trip requests into structured itineraries.

System Flow:

Frontend → Backend → AI Service → Database

## Components

### Frontend
React + Vite application.

Responsibilities:
- user interface
- trip input
- itinerary visualization
- wishlist management
- collaboration interface
- route visualization

### Backend
Node.js + Express API.

Responsibilities:
- handle frontend requests
- interact with AI service
- manage database queries
- handle collaboration sessions

### AI Service
Python FastAPI microservice.

Responsibilities:
- intent extraction from user query
- recommendation filtering
- itinerary generation
- route optimization

### Database
Stores verified travel catalog data.

Tables:
- hotels
- places
- activities
- events

## Architecture Diagram

User
↓
Frontend (React)
↓
Backend API (Node)
↓
AI Service (FastAPI)
↓
Database (Travel Catalog)

""",

"api-spec.md": """
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

""",

"dataset.md": """
# Travel Catalog Dataset

## Purpose

The system must use **verified catalog data** for recommendations.

This dataset will contain travel-related entities.

---

## Tables

### Places

| Field | Description |
|------|-------------|
id | unique id |
name | place name |
location | city/location |
category | type |
rating | rating |

---

### Hotels

| Field | Description |
|------|-------------|
id | unique id |
name | hotel name |
location | city |
price | price range |
rating | rating |

---

### Activities

| Field | Description |
|------|-------------|
id | unique id |
name | activity |
location | place |
category | adventure/culture |
price | cost |

---

## Data Sources

Possible sources:

- Kaggle tourism datasets
- Open travel APIs
- curated datasets

""",

"pitch.md": """
# TravelMind Pitch Notes

## Problem

Travel planning is fragmented.

Users search separately for:
- hotels
- activities
- events
- travel routes

Planning becomes time-consuming.

---

## Solution

TravelMind is an AI-powered travel planner.

User enters natural language request:

"Plan a 3 day Goa trip under 20k"

System automatically:

- extracts trip intent
- recommends hotels and activities
- generates itinerary
- optimizes route
- enables collaboration

---

## Demo Flow

1. User enters trip request
2. AI extracts trip parameters
3. System generates itinerary
4. Map displays optimized route
5. User saves items to wishlist
6. Friends collaborate on planning

---

## Impact

TravelMind simplifies travel planning by integrating
multiple services into a single intelligent platform.

Benefits:

- reduces planning time
- improves travel platform engagement
- scalable AI travel planning engine

"""
}


def create_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for filename, content in files.items():
        path = os.path.join(DOCS_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())

        print(f"Created: {path}")


def git_commit_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "docs: add architecture, api, dataset and pitch documentation"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("Git commit and push successful.")
    except subprocess.CalledProcessError:
        print("Git operation failed. Check git configuration.")


if __name__ == "__main__":
    create_docs()
    git_commit_push()