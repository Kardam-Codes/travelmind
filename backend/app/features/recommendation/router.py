from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.recommendation.service import get_recommendations
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", response_model=RecommendationResponse)
def get_recommendations_endpoint(
    request_data: RecommendationRequest,
    session: Session = Depends(get_session),
):
    return get_recommendations(session, request_data)
