from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.constants import HEALTH_STATUS_OK
from app.core.logging import setup_logging
from app.database.base import create_db_and_tables


logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logger.info("Database tables initialized.")
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
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
