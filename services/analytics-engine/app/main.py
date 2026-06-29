"""GuideU analytics-engine — FastAPI application factory.

Serves anti-scam scoring, route recommendations, guide ranking and price
benchmarking. Boots and serves with only pandas + scikit-learn; trained model
artifacts are loaded lazily from the registry when present (ADR-0006).
"""
from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.config import get_settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

DESCRIPTION = """
GuideU's machine-learning service.

Sprint 1 ships the service foundation: a health/liveness probe and the model
registry. Inference endpoints (anti-scam, recommendations, guide ranking,
pricing) are delivered from sprint-2 onward. Internal endpoints require the
`X-API-Key` header.
""".strip()


def create_app() -> FastAPI:
    get_settings()  # ensure artifact dir exists, fail fast on bad config
    app = FastAPI(
        title="GuideU Analytics Engine",
        version="1.0.0",
        description=DESCRIPTION,
        contact={"name": "GuideU"},
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)

    @app.get("/", tags=["health"])
    async def index() -> dict:
        return {"service": "guideu-analytics-engine", "docs": "/docs", "health": "/health"}

    return app


app = create_app()
