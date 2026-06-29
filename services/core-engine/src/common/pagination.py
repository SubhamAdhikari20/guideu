from __future__ import annotations

from rest_framework.pagination import CursorPagination, PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    """Default page-number pagination with a client-controllable page size."""

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class TimelineCursorPagination(CursorPagination):
    """Stable cursor pagination for high-write feeds (notifications, events)."""

    page_size = 25
    ordering = "-created_at"
    page_size_query_param = "page_size"
    max_page_size = 100
