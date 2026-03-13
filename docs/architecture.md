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