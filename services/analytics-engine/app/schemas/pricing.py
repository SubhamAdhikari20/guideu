from __future__ import annotations

from pydantic import BaseModel, Field


class BenchmarkRequest(BaseModel):
    service_type: str = Field(..., examples=["Porter"])
    region: str | None = Field(None, examples=["Langtang"])
    season: str | None = Field(None, examples=["Peak (Spring)"])


class BenchmarkResponse(BaseModel):
    service_type: str
    region: str | None
    season: str | None
    fair_price_npr: int
    min_fair_npr: int
    max_fair_npr: int
    currency: str
    granularity: str


class ModelCardOut(BaseModel):
    name: str
    version: str
    metrics: dict[str, float]
    params: dict
    trained_at: str
    n_train: int
    notes: str
