from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers (you will create these later)
from app.features.trip_planning.trip_router import router as trip_router
from app.features.recommendation.recommendation_router import router as recommendation_router
from app.features.wishlist.wishlist_router import router as wishlist_router
from app.features.collaboration.websocket_router import router as websocket_router


app = FastAPI(
    title="TravelMind Backend",
    version="0.1.0",
    description="AI-powered travel planning backend",
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Root Endpoints
# -----------------------------
@app.get("/")
def root():
    return {"message": "TravelMind backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Include Feature Routers
# -----------------------------
app.include_router(trip_router, prefix="/api/trip", tags=["Trip"])
app.include_router(recommendation_router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(wishlist_router, prefix="/api/wishlist", tags=["Wishlist"])
app.include_router(websocket_router, tags=["Collaboration"])