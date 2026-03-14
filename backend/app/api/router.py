from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.cities.router import router as cities_router
from app.features.collaboration.router import router as collaboration_router
from app.features.comments.router import router as comments_router
from app.features.bookings.router import router as bookings_router
from app.features.invites.router import router as invites_router
from app.features.itinerary.router import router as itinerary_router
from app.features.maps.router import router as maps_router
from app.features.orgs.router import router as orgs_router
from app.features.recommendation.router import router as recommendation_router
from app.features.reports.router import router as reports_router
from app.features.trip_planning.router import router as trip_router
from app.features.wishlist.router import router as wishlist_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(cities_router)
api_router.include_router(trip_router)
api_router.include_router(recommendation_router)
api_router.include_router(itinerary_router)
api_router.include_router(maps_router)
api_router.include_router(wishlist_router)
api_router.include_router(collaboration_router)
api_router.include_router(orgs_router)
api_router.include_router(invites_router)
api_router.include_router(comments_router)
api_router.include_router(bookings_router)
api_router.include_router(reports_router)
