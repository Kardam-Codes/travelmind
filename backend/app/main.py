from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.constants import HEALTH_STATUS_OK
from app.core.logging import setup_logging
from app.database.base import create_db_and_tables
from app.database.seed import seed_reference_data


logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_reference_data()
    logger.info("Database tables initialized.")
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_origin_regex=settings.cors_origin_regex or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health_check():
    return {
        "status": HEALTH_STATUS_OK,
        "app_name": settings.app_name,
    }
