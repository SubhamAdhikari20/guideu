"""Viewset mixins that enforce ownership scoping by default."""
from __future__ import annotations

from typing import Any


class OwnedQuerySetMixin:
    """Restrict list/detail to objects owned by the requesting user.

    Staff users see everything. Set ``owner_field`` on the viewset (default
    ``user``). Combine with :class:`common.permissions.IsOwnerOrReadOnly`.
    """

    owner_field: str = "user"

    def get_queryset(self):  # type: ignore[override]
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if user.is_staff:
            return queryset
        return queryset.filter(**{self.owner_field: user})


class AutoOwnerMixin:
    """Inject the requesting user as the owner on create."""

    owner_field: str = "user"

    def perform_create(self, serializer: Any) -> None:  # type: ignore[override]
        serializer.save(**{self.owner_field: self.request.user})
