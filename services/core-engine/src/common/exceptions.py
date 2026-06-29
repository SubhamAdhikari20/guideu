"""Consistent API error envelope.

Every handled error returns the same shape so clients (Flutter, Next.js) can
parse failures uniformly::

    { "error": { "type": "validation_error", "detail": {...}, "status": 400 } }
"""
from __future__ import annotations

import logging
from typing import Any

from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("guideu.api")


def api_exception_handler(exc: Exception, context: dict[str, Any]):
    response = drf_exception_handler(exc, context)
    if response is None:
        # Unhandled exception — log with context; DRF/Django will 500.
        view = context.get("view")
        logger.exception("Unhandled API exception in %s", getattr(view, "__class__", None))
        return None

    response.data = {
        "error": {
            "type": exc.__class__.__name__.replace("Exception", "").replace("Error", "").lower()
            or "error",
            "detail": response.data,
            "status": response.status_code,
        }
    }
    return response
