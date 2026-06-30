from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import require_api_key
from app.schemas.recommendations import RecommendRequest, RecommendResponse
from inference import recommender

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"], dependencies=[Depends(require_api_key)])


@router.post("/routes", response_model=RecommendResponse)
async def recommend_routes(payload: RecommendRequest) -> RecommendResponse:
    """Personalised, explainable route ranking for a tourist profile."""
    result = recommender.recommend(
        tourist=payload.tourist.model_dump(),
        season=payload.season,
        top_k=payload.top_k,
    )
    return RecommendResponse(**result)
