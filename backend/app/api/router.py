from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.collaboration.router import router as collaboration_router
from app.features.itinerary.router import router as itinerary_router
from app.features.recommendation.router import router as recommendation_router
from app.features.trip_planning.router import router as trip_router
from app.features.wishlist.router import router as wishlist_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(trip_router)
api_router.include_router(recommendation_router)
api_router.include_router(itinerary_router)
api_router.include_router(wishlist_router)
api_router.include_router(collaboration_router)
