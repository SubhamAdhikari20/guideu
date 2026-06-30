from __future__ import annotations

from pydantic import BaseModel, Field


class ScamScoreRequest(BaseModel):
    service_type: str = Field(..., examples=["Licensed Guide"])
    region: str | None = Field(None, examples=["Everest/Khumbu"])
    season: str | None = Field(None, examples=["Peak (Autumn)"])
    quoted_price_npr: float = Field(..., gt=0, examples=[9000])


class ScamScoreResponse(BaseModel):
    scam_probability: float
    is_likely_scam: bool
    severity: str | None
    benchmark_price_npr: int | None
    overcharge_ratio: float | None
    model_version: str
    explanation: list[str]
