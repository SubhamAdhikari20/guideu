from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import require_api_key
from app.schemas.pricing import BenchmarkRequest, BenchmarkResponse, ModelCardOut
from inference import pricing
from registry import list_models

router = APIRouter(prefix="/api/v1", tags=["pricing"], dependencies=[Depends(require_api_key)])


@router.post("/pricing/benchmark", response_model=BenchmarkResponse)
async def benchmark(payload: BenchmarkRequest) -> BenchmarkResponse:
    """Fair-price range for a service (transparent pricing)."""
    result = pricing.fair_price(payload.service_type, payload.region, payload.season)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No benchmark for this service.")
    return BenchmarkResponse(**result)


@router.get("/models", response_model=list[ModelCardOut])
async def models() -> list[ModelCardOut]:
    """The model registry — versions, metrics, training metadata."""
    return [
        ModelCardOut(
            name=c.name, version=c.version, metrics=c.metrics, params=c.params,
            trained_at=c.trained_at, n_train=c.n_train, notes=c.notes,
        )
        for c in list_models()
    ]
