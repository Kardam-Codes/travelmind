from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.repositories.city_repository import get_all_cities
from app.schemas.city import CityRead


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=List[CityRead])
def list_cities_endpoint(session: Session = Depends(get_session)):
    cities = get_all_cities(session)
    response = []
    for city in cities:
        payload = city.model_dump(exclude={"image_url"})
        payload["image_url"] = city.image_url or ""
        response.append(CityRead(**payload))
    return response
