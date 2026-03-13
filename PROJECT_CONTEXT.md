# TravelMind — Project Context

## Project Name
TravelMind – AI Powered Travel Guide & Itinerary Builder

## Hackathon Project

TravelMind is being developed for a hackathon where the objective is to build an **AI-powered travel planning platform** that converts natural language travel requests into structured travel itineraries.

The system should recommend hotels, activities, and experiences based on verified catalog data and generate a day-by-day itinerary automatically.

---

# Core Problem

Travel planning is currently fragmented.

Users must manually browse multiple platforms for:

- hotels
- tourist places
- activities
- events
- travel routes

This process is time consuming and inefficient.

There is a need for a system that **automatically generates a structured travel plan from a simple natural language request**.

---

# Our Solution

TravelMind is an AI-powered travel planning platform that:

1. Accepts natural language travel requests
2. Uses AI to extract trip parameters
3. Recommends travel options from a catalog dataset
4. Generates a structured day-by-day itinerary
5. Optimizes travel routes using map APIs
6. Enables real-time collaborative trip planning

Example Input:

Plan a 3 day Goa trip under ₹20000 for friends

Example Output:

Day 1
- Hotel check-in
- Beach visit
- Local market

Day 2
- Water sports
- Sunset point

Day 3
- Cultural sites

---

# Target Users

TravelMind is designed for:

- Individual travelers
- Groups of friends
- Families planning vacations

---

# Key Features

## 1 Natural Language Trip Planning

Users describe travel plans in plain English.

Example:

Plan a 4 day Manali trip under ₹15000

---

## 2 AI Intent Extraction

The AI system extracts structured trip parameters.

Extracted fields:

- destination
- duration
- budget
- preferences
- group type

---

## 3 Recommendation Engine

The system recommends travel options using a catalog dataset.

Catalog includes:

- hotels
- tourist places
- activities
- events

---

## 4 AI Itinerary Generation

Hybrid AI approach:

Step 1  
LLM extracts trip parameters.

Step 2  
Python algorithm generates itinerary using catalog data.

---

## 5 Route Optimization

Travel routes are optimized using:

- Google Maps Distance Matrix API
- Google Maps Directions API

This minimizes travel time between itinerary locations.

---

## 6 Real-Time Collaboration

Multiple users can collaborate on the same trip.

Features:

- edit itinerary
- vote on activities
- synchronize updates

Implemented using:

FastAPI WebSockets

---

# Final Architecture

User
 │
 ▼
Natural Language Input
 │
 ▼
React Frontend (Vite)
 │
 ▼
FastAPI Backend
 │
 ├─ Intent Extraction
 ├─ Recommendation Engine
 ├─ Itinerary Generator
 ├─ Route Optimization
 └─ WebSocket Collaboration
 │
 ├─ PostgreSQL Database
 │    ├ hotels
 │    ├ places
 │    ├ activities
 │    └ events
 │
 └─ Google Maps API
      ├ Distance Matrix
      └ Directions API

---

# Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- Google Maps API

---

## Backend

- FastAPI
- SQLModel
- WebSockets

---

## Database

- PostgreSQL

---

## AI Layer

- LLM API
- Python recommendation engine
- Python itinerary generation algorithm

---

# Backend Architecture

Backend and AI logic are merged into one FastAPI service.

Reasons:

- Python preferred by backend developers
- easier integration between AI and API
- faster development during hackathon

---

# Backend Folder Structure

backend/

app/
main.py

features/

trip_planning/
router.py
service.py
schema.py

recommendation/
router.py
engine.py
schema.py

itinerary/
generator.py
router.py

collaboration/
websocket.py
manager.py

database/
connection.py
models.py

utils/
maps.py
helpers.py

requirements.txt

---

# Database Technology

Using:

SQLModel + PostgreSQL

Reasons:

- less boilerplate
- easier FastAPI integration
- faster development

---

# Real-Time Collaboration

Implemented using:

FastAPI WebSockets

WebSocket endpoint:

/ws/trip/{trip_id}

Supported events:

JOIN_TRIP  
UPDATE_ITINERARY  
VOTE_ACTIVITY  
SYNC_STATE  

---

# Documentation

The project contains documentation in `docs/`.

Files include:

docs/

architecture.md  
api-spec.md  
dataset.md  
pitch.md  
service-contract.md  
backend-spec.md  
architecture-diagram.png  

---

# Development Status

Completed:

✔ GitHub repository created  
✔ Architecture designed  
✔ Documentation created  
✔ Backend skeleton generated  
✔ FastAPI chosen as backend framework  
✔ SQLModel chosen for database  
✔ WebSockets chosen for collaboration  
✔ Google Maps chosen for route optimization  

---

# Team Roles

## Jay

Responsibilities:

- Frontend development
- React UI components
- Map visualization
- Collaboration UI

---

## Kardam

Responsibilities:

- Product planning
- Dataset preparation
- Documentation
- Testing
- Architecture decisions

---

## Misha

Responsibilities:

- FastAPI backend development
- Database models
- API endpoints

---

## Yug

Responsibilities:

- AI logic
- intent extraction
- recommendation engine
- itinerary generation algorithm

---

# Coding Rules

The project uses **feature-based architecture**.

Each file must contain metadata headers.

Example header:

Feature:
File Purpose:
Owner:
Dependencies:
Last Updated:

---

# Next Development Tasks

## Backend

- implement LLM intent extraction
- implement recommendation engine
- implement itinerary generator
- implement database models
- implement WebSocket collaboration manager

---

## Frontend

- trip input UI
- itinerary dashboard
- map visualization
- collaborative editing

---

## AI

Algorithm design:

LLM → extract parameters

Python → generate itinerary using catalog data

---

# End of Project Context

This document defines the current system architecture, stack, roles, and development status.

All development must follow the architecture and structure defined here.
