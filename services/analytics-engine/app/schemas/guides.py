from __future__ import annotations

from pydantic import BaseModel, Field

from .recommendations import TouristProfileIn


class GuideRankRequestTourist(TouristProfileIn):
    region: str | None = Field(None, examples=["Everest/Khumbu"])
    language: str | None = Field(None, examples=["English"])


class GuideCandidate(BaseModel):
    guide_id: str | None = None
    certification: str = Field(..., examples=["IFMGA Mountain Guide"])
    average_rating: float = Field(0, ge=0, le=5)
    regions_covered: str | None = None
    languages_spoken: str | None = None


class GuideRankRequest(BaseModel):
    tourist: GuideRankRequestTourist
    candidates: list[GuideCandidate]


class RankedGuide(GuideCandidate):
    score: float
    components: dict[str, float]


class GuideRankResponse(BaseModel):
    model_version: str
    items: list[RankedGuide]
