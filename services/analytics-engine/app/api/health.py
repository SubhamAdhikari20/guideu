from __future__ import annotations

from fastapi import APIRouter

from registry import list_models

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Liveness probe + currently registered model versions."""
    models = {card.name: card.version for card in list_models()}
    return {"status": "healthy", "service": "guideu-analytics-engine", "models": models}
