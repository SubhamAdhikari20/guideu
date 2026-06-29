from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import require_api_key
from app.schemas.guides import GuideRankRequest, GuideRankResponse
from inference import guides as guides_inference

router = APIRouter(prefix="/api/v1/guides", tags=["guides"], dependencies=[Depends(require_api_key)])


@router.post("/rank", response_model=GuideRankResponse)
async def rank_guides(payload: GuideRankRequest) -> GuideRankResponse:
    """Rank candidate guides for a tourist's request (transparent scoring)."""
    result = guides_inference.rank(
        tourist=payload.tourist.model_dump(),
        candidates=[c.model_dump() for c in payload.candidates],
    )
    return GuideRankResponse(**result)
