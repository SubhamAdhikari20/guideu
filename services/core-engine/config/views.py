"""Top-level non-API views: a service index and a liveness probe."""
from __future__ import annotations

from django.http import JsonResponse


def service_index(request) -> JsonResponse:
    """Human-friendly index of the core engine's entry points."""
    return JsonResponse(
        {
            "service": "guideu-core-engine",
            "status": "ok",
            "docs": "/api/docs/",
            "schema": "/api/schema/",
            "admin": "/admin/",
            "api_root": "/api/v1/",
        }
    )


def healthz(request) -> JsonResponse:
    """Liveness probe used by orchestrators."""
    return JsonResponse({"status": "healthy"})
