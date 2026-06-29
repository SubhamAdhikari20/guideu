from __future__ import annotations

from pydantic import BaseModel, Field


class TouristProfileIn(BaseModel):
    pref_adventure_score: float = Field(0.5, ge=0, le=1)
    pref_culture_score: float = Field(0.5, ge=0, le=1)
    pref_nature_score: float = Field(0.5, ge=0, le=1)
    budget_band: str | None = Field(None, examples=["Mid-range"])
    fitness_level: str | None = Field(None, examples=["Good"])


class RecommendRequest(BaseModel):
    tourist: TouristProfileIn
    season: str | None = Field(None, examples=["Autumn"])
    top_k: int = Field(5, ge=1, le=50)


class RouteRecommendation(BaseModel):
    route_id: str
    route_name: str
    region: str
    difficulty: str
    score: float
    components: dict[str, float]


class RecommendResponse(BaseModel):
    model_version: str
    items: list[RouteRecommendation]
