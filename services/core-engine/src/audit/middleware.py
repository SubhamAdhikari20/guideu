"""Middleware that records state-changing API requests to the audit trail.

Only mutating requests (POST/PUT/PATCH/DELETE) under ``/api/`` are recorded, so
read traffic stays cheap. Writing the log row is best-effort: an audit failure
must never break the user's request.
"""
from __future__ import annotations

import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("guideu.audit")

_AUDITED_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _client_ip(request: HttpRequest) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class RequestAuditMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if request.method in _AUDITED_METHODS and request.path.startswith("/api/"):
            self._record(request, response)
        return response

    def _record(self, request: HttpRequest, response: HttpResponse) -> None:
        try:
            from .models import AuditLog

            user = getattr(request, "user", None)
            AuditLog.objects.create(
                actor=user if (user and user.is_authenticated) else None,
                method=request.method,
                path=request.path[:512],
                status_code=response.status_code,
                ip_address=_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
            )
        except Exception as exc:  # pragma: no cover - never break the response
            logger.debug("audit record failed: %s", exc)
