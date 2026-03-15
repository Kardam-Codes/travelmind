# TravelMind

An AI-powered travel planning studio that turns natural language into a structured itinerary, with verified catalog data, live collaboration, and a map-first experience.

## Why it’s unique
- **Map-first planning**: Real routes + ordered stops tied to itinerary edits.
- **Verified catalog only**: Recommendations are grounded in your dataset, not random web results.
- **Collaborative by design**: Live chat, locking, and versioned edits for group planning.
- **Unknown-city fallback**: Generates a city pack when the destination isn’t in the dataset.
- **Premium UX**: A planning studio feel, not a form-heavy dashboard.

## Stack
- **Frontend**: React + Vite + Tailwind
- **Backend**: FastAPI + SQLModel + Postgres
- **AI service**: FastAPI (local or hosted)
- **Maps**: Leaflet + OSRM routing

## Repos/Services
- `frontend/` – Vite app
- `backend/` – FastAPI app
- `ai-service/` – intent extraction and city-pack generation
- `datasets/` – cities, places, hotels, activities

## Quick Start (Local)

### 1) Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2) AI Service (optional)
```bash
cd ai-service/app
python -m venv .venv
.\.venv\Scripts\activate
pip install -r ..\requirements.txt
python main.py
```

### 3) Frontend
```bash
cd frontend
npm install
npm run dev
```

## Env Variables

### Backend
```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
JWT_SECRET=your-secret
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
AI_SERVICE_BASE_URL=http://127.0.0.1:8001
ROUTING_BASE_URL=https://router.project-osrm.org
```

### Frontend
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Manual Image URL Update (Cities, Activities, Places)

If you updated `datasets/*.csv` with `image_url`, run:
```bash
cd backend
set DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
python -m app.database.update_images
```

This updates existing DB rows without wiping data.

## Demo Flow (Judges)
1. Sign up / log in
2. Plan your first trip
3. View planner (map + itinerary)
4. Edit itinerary and see live map updates
5. Explore destinations

## Deployment (Quick)
1. Deploy `ai-service` (Render)
2. Deploy `backend` (Render) with `DATABASE_URL`
3. Deploy `frontend` (Vercel) with `VITE_API_BASE_URL`

## Notes
- If images are missing on Explore or planner, run the manual image update script above.
- If CORS fails, ensure `CORS_ORIGINS` includes your Vercel URL.
