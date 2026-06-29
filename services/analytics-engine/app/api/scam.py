from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import require_api_key
from app.schemas.scam import ScamScoreRequest, ScamScoreResponse
from inference import scam as scam_inference

router = APIRouter(prefix="/api/v1/scam", tags=["anti-scam"], dependencies=[Depends(require_api_key)])


@router.post("/score", response_model=ScamScoreResponse)
async def score(payload: ScamScoreRequest) -> ScamScoreResponse:
    """Score a quoted price for overcharge / scam risk, with an explanation."""
    result = scam_inference.score(
        service_type=payload.service_type,
        region=payload.region,
        season=payload.season,
        quoted_price_npr=payload.quoted_price_npr,
    )
    return ScamScoreResponse(**result)
